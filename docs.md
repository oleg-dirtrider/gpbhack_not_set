# Вопросы
1. Процессы это общее понятие, они бывают 3 видов  
    1. Дата-процесс
    2. sas-процесс
    3. web-процесс
2. Библиотеки это коллекции таблиц бд которые используются в data-processes  

# Сущности SAS
- Компания(стратегия, диаграмма) 
    - Блоки, узлы(могут содержать в себе другие диаграммы в виде Subdiagram)
      - Subdiagram
      - Process
        - data-process 
        - sas-process
        - web-process
      - Event  
      - .....
  - ...
- ...  
  
Узлы могу содержать процессы, один узел-один процесс(узлы процессов)
    
# Результат
Результат пишется в таблички бд со следующей структурой:
    
- campaigns(id(CampaignDO.Id), campaign_name) -> хранит компании sas rtdm
- blocks(id(ProcessNodeDataDO.NodeId), block_name, block_type, subdiagram_id, campaign_id) -> хранит блоки компании, имеет внешний ключ на таблику campaign.id
- data_process(id(ProcessNodeDataDO.Process.Id), data_process_name, block_id, lib_name, table_name) -> хранит дата-процессы, и
  меет внешний ключ на таблику blocks.id

# Архитектура
## Основные модули
- парсер xml  
    - **вход** : xml-файл  
    - **выход** : словарь со списками дата-классов для записи в бд
    ```json
      {
        "campaigns": [
          "{data_class_instance}", 
           ...
        ],
        "blocks": [
          "{data_class_instance}", 
           ...
        ],
        "data_processes": [
          "{data_class_instance}", 
           ...
        ]
      }
    ```
    - **ограничения**: необходимо следить за консистентностью данных(внешние ключи)
  
- интерфейс запуска
  - **вход** : аргументы командной строки  
  - **выход** : None или сообщение 
  - **ограничения**: -
  
- запись результата в бд
  - **вход** : выход парсера xml
    ```json
      {
        "campaigns": [
          "{data_class_instance}", 
           ...
        ],
        "blocks": [
          "{data_class_instance}", 
           ...
        ],
        "data_process": [
          "{data_class_instance}", 
           ...
        ]
      }
    ```
  - **выход** : None или сообщение 
  - **ограничения**: -
