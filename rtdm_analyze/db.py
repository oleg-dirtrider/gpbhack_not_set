import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import registry, relationship, Session


mapper_registry = registry()
Base = mapper_registry.generate_base()


SCHEMA = "RTDM_TECH"

db_url = os.getenv("RTDM_ANALYZER_DB_URL")


campaigns_blocks_data_processes_association_table = Table(
    'campaigns_blocks_data_processes_association', mapper_registry.metadata,
    Column('campaign_block', Integer, ForeignKey(f'{SCHEMA}.campaigns_blocks.id'), nullable=False),
    Column('data_process', Integer, ForeignKey(f'{SCHEMA}.data_processes.id'), nullable=False),
    schema=SCHEMA
)


class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, nullable=False)
    sas_campaign_id = Column(String, nullable=False)
    campaign_name = Column(String)
    campaigns_blocks = relationship("CampaignBlock", back_populates="campaign")

    def __repr__(self):
        return \
            f"Campaign(id={self.id!r}, sas_campaign_id={self.sas_campaign_id!r}, campaign_name={self.campaign_name!r})"


class CampaignBlock(Base):
    __tablename__ = "campaigns_blocks"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, nullable=False)
    sas_block_id = Column(String, nullable=False)
    block_name = Column(String)
    block_type = Column(String)
    subdiagram_id = Column(String)
    subdiagram_name = Column(String)
    campaign_id = Column(Integer, ForeignKey(f'{SCHEMA}.campaigns.id'), nullable=False)
    campaign = relationship("Campaign", back_populates="campaigns_blocks")
    data_processes = relationship(
        "DataProcess", secondary=campaigns_blocks_data_processes_association_table, back_populates='campaigns_blocks'
    )

    def __repr__(self):
        return f"Campaign(id={self.id!r}, sas_block_id={self.sas_block_id!r}, block_name={self.block_name!r})"


class DataProcess(Base):
    __tablename__ = "data_processes"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, nullable=False)
    sas_data_process_id = Column(String, nullable=False)
    data_process_name = Column(String)
    lib_name = Column(String)
    table_name = Column(String)
    campaigns_blocks = relationship(
        "CampaignBlock", secondary=campaigns_blocks_data_processes_association_table, back_populates="data_processes"
    )

    def __repr__(self):
        return f"Campaign(id={self.id!r}, sas_data_process_id={self.sas_data_process_id!r}, " \
               f"data_process_name={self.data_process_name!r})"


class DBRunner:
    def __init__(self, connection_string: str = db_url) -> None:
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string, future=True)
        #mapper_registry.metadata.create_all(self.engine)

    def clear_tables(self):
        sql = """
            delete from RTDM_TECH.campaigns_blocks_data_processes_association;
            delete from RTDM_TECH.data_processes;
            delete from RTDM_TECH.campaigns_blocks;
            delete from RTDM_TECH.campaigns;
        """
        session = Session(self.engine)
        session.execute(sql)
        session.commit()
        session.close()

    def get_all_data_processes(self):
        session = Session(self.engine)
        data_processes_list = [data_process.data_process_name for data_process in session.query(DataProcess).all()]
        session.close()
        return data_processes_list

    def insert_data(self, data: dict):
        session = Session(self.engine)
        campaign_dict = {}
        block_dict = {}
        for row in data["campaigns"]:
            row_instance = Campaign(
                sas_campaign_id=row.id,
                campaign_name=row.name,
            )
            session.add(row_instance)
            session.flush()
            campaign_dict[row_instance.sas_campaign_id] = row_instance.id
        for row in data["blocks"]:
            row_instance = CampaignBlock(
                sas_block_id=row.id,
                block_name=row.name,
                block_type=row.type,
                subdiagram_id=row.subdiagram_id,
                subdiagram_name=row.subdiagram_name,
                campaign_id=campaign_dict[row.campaign_id],
            )
            session.add(row_instance)
            session.flush()
            block_dict[row_instance] = row.data_process_id_list
        data_process_list = []
        for row in data["data_processes"]:
            row_instance = DataProcess(
                sas_data_process_id=row.id,
                data_process_name=row.name,
                lib_name=row.lib_name,
                table_name=row.table_name
            )
            data_process_campaign_block = []
            for campaign_block_instance, data_processes_id_list in block_dict.items():
                if row_instance.sas_data_process_id in data_processes_id_list:
                    data_process_campaign_block.append(campaign_block_instance)
            row_instance.campaigns_blocks = data_process_campaign_block
            data_process_list.append(row_instance)
        session.add_all(data_process_list)
        session.commit()
        session.close()

    def get_columns_of_table(self, table_name: str):
        sql = F"""
            select t.name table_name, c.name column_name 
            from sys.tables t join sys.columns c on t.object_id = c.object_id
            where t.name = '{table_name}';
        """
        session = Session(self.engine)
        result = session.execute(sql)
        return [row[1] for row in result]

    def check(self, data_procces_list: list):
        table_dict = {}
        for data_process in data_procces_list:
            db_column_names = self.get_columns_of_table(data_process.table_name)
            for d_p_col in data_process.columns:
                if d_p_col["name"] not in db_column_names:
                    table_dict[data_process.name] = (data_process.table_name, d_p_col)

        return table_dict