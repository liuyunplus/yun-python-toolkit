import pymysql
import stringutils
import textwrap
from jinja2 import Template


mysql_java_map = {
    "varchar": "String",
    "int": "Integer",
    "tinyint": "Integer",
    "bigint": "Long",
    "float": "Float",
    "double": "Double",
    "bit": "Boolean",
    "decimal": "BigDecimal",
    "datetime": "Date",
    "timestamp": "Date",
}


def main(table_name):
    db = pymysql.connect(host='172.16.103.106', port=3306, user='root', password='123456', database='vivid_meetup')
    cursor = db.cursor()
    sql = "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = database() and TABLE_NAME = '{table_name}'".format(table_name=table_name)
    cursor.execute(sql)
    result = cursor.fetchall()
    field_list = []
    for field in result:
        column_name = field[0]
        column_type = field[1]
        if column_name == "id" or column_name == "created" or column_name == "updated":
            continue
        data = {
            "column_name": column_name,
            "field_name": stringutils.snake_to_camel(column_name),
            "field_type": mysql_java_map.get(column_type)
        }
        field_list.append(data)
    cursor.close()
    db.close()
    generate_do(table_name, field_list)
    generate_repository(table_name)


def generate_do(table_name, field_list):
    class_name = stringutils.snake_to_pascal(table_name.replace("t_", "")) + "DO"
    tmpl = """
        import javax.persistence.Column;
        import javax.persistence.Entity;
        import javax.persistence.Table;

        @Entity
        @Table(name="{{ table_name }}")
        public class {{ class_name }} extends BaseDO {
            {% for field in field_list %}
            @Column(name = "{{ field['column_name'] }}")
            private {{ field['field_type'] }} {{ field['field_name'] }};
            {% endfor %}
        }
        """
    template = Template(textwrap.dedent(tmpl))
    content = template.render(table_name=table_name, class_name=class_name, field_list=field_list)
    print(content)


def generate_repository(table_name):
    class_name = stringutils.snake_to_pascal(table_name.replace("t_", ""))
    repository_name = class_name + "Repository"
    dao_name = class_name + "DO"
    tmpl = """
    import org.springframework.data.jpa.repository.JpaRepository;
    import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
    
    public interface {{ repository_name }} extends JpaRepository<{{ dao_name }}, Long>, JpaSpecificationExecutor<{{ dao_name }}> {
        
    }
    """
    template = Template(textwrap.dedent(tmpl))
    content = template.render(repository_name=repository_name, dao_name=dao_name)
    print(content)


main("t_activity_member")