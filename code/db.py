from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship, Session


mapper_registry = registry()
Base = mapper_registry.generate_base()

# mapper_registry.metadata.create_all(engine)

SCHEMA = "RTDM_TECH"

db_url = "mssql+pyodbc://Team8:Team81!ijn@c2-185-12-28-165.elastic.cloud.croc.ru:1433/db_Team8?" \
         "driver=SQL+Server+Native+Client+11.0"


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
    campaign_id = Column(Integer, ForeignKey(f'{SCHEMA}.campaigns.id'), nullable=False)
    campaign = relationship("Campaign", back_populates="campaigns_blocks")
    data_process_id = Column(Integer, ForeignKey(f"{SCHEMA}.data_processes.id"), nullable=False)
    data_process = relationship("DataProcess", back_populates="campaigns_blocks")

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
    campaigns_blocks = relationship("CampaignBlock", back_populates="data_process")

    def __repr__(self):
        return f"Campaign(id={self.id!r}, sas_data_process_id={self.sas_data_process_id!r}, " \
               f"data_process_name={self.data_process_name!r})"


class DBRunner:
    def __init__(self, connection_string: str = "sqlite+pysqlite:///gpbhack.db") -> None:
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string, echo=True, future=True)

    def insert_data(self, data: dict):
        session = Session(self.engine)
        # table_map = {
        #     "blocks": Campaign,
        #     "campaigns": CampaignBlock,
        #     "data_process": DataProcess
        # }
        campaign_dict = {}
        data_process_dict = {}
        for row in data["campaigns"]:
            row_instance = Campaign(
                sas_campaign_id=row.id,
                campaign_name=row.name,
            )
            session.add(row_instance)
            session.flush()
            campaign_dict[row_instance.sas_campaign_id] = row_instance.id
        for row in data["data_processes"]:
            row_instance = DataProcess(
                sas_data_process_id=row.id,
                data_process_name=row.name,
                lib_name=row.lib_name,
                table_name=row.table_name
            )
            session.add(row_instance)
            session.flush()
            data_process_dict[row_instance.sas_data_process_id] = row_instance.id
        for row in data["blocks"]:
            row_instance = CampaignBlock(
                sas_block_id=row.id,
                block_name=row.name,
                block_type=row.type,
                subdiagram_id=row.subdiagram_id,
                campaign_id=campaign_dict[row.campaign_id],
                data_process_id=data_process_dict.get(row.data_process_id, 1)
            )
            session.add(row_instance)
            session.flush()



        # c = Campaign(
        #     sas_campaign_id='test',
        #     campaign_name = "test",
        # )
        # d = DataProcess(
        #     sas_data_process_id = "test",
        #     data_process_name = "test",
        #     lib_name = "test",
        #     table_name = "test",
        # )
        # b = CampaignBlock(
        #     sas_block_id="test",
        #     block_name = "test",
        #     block_type = "test",
        #     subdiagram_id = "test",
        #     campaign_id = 1,
        #     data_process_id = 1
        # )
        # session.add(c)
        # session.add(d)
        # session.flush()
        # session.add(b)
        session.commit()
        session.close()




