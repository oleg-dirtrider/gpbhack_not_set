select * from RTDM_TECH.campaigns c join RTDM_TECH.campaigns_blocks b on c.id = b.campaign_id;

select c.campaign_name, count(b.id) as block_numbers
from RTDM_TECH.campaigns c join RTDM_TECH.campaigns_blocks b on c.id = b.campaign_id
group by c.campaign_name;

select b.block_name, b.block_type, b.subdiagram_name, d.data_process_name, d.lib_name, d.table_name
from RTDM_TECH.campaigns_blocks b join RTDM_TECH.campaigns_blocks_data_processes_association a on b.id=a.campaign_block
    join RTDM_TECH.data_processes d on a.data_process=d.id
order by b.id;


select c.campaign_name,  b.block_name, count(d.id) data_process_number
from RTDM_TECH.campaigns c join RTDM_TECH.campaigns_blocks b on c.id = b.campaign_id
    join RTDM_TECH.campaigns_blocks_data_processes_association a on b.id=a.campaign_block
    join RTDM_TECH.data_processes d on a.data_process=d.id
group by c.campaign_name, b.block_name
order by c.campaign_name, b.block_name;


select c.campaign_name, count(d.id) data_process_number
from RTDM_TECH.campaigns c join RTDM_TECH.campaigns_blocks b on c.id = b.campaign_id
    join RTDM_TECH.campaigns_blocks_data_processes_association a on b.id=a.campaign_block
    join RTDM_TECH.data_processes d on a.data_process=d.id
group by c.campaign_name
order by c.campaign_name;


select c.campaign_name, d.table_name
from RTDM_TECH.campaigns c join RTDM_TECH.campaigns_blocks b on c.id = b.campaign_id
    join RTDM_TECH.campaigns_blocks_data_processes_association a on b.id=a.campaign_block
    join RTDM_TECH.data_processes d on a.data_process=d.id
order by c.campaign_name;