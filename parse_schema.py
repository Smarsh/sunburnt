import lxml.etree

class solr_date(object):
    pass

solr_data_types = {
    'solr.StrField':str,
    'solr.TextField':str,
    'solr.BoolField':bool,
    'solr.IntField':int,
    'solr.SortableIntField':int,
    'solr.LongField':long,
    'solr.SortableLongField':long,
    'solr.FloatField':float,
    'solr.SortableFloatField':float,
    'solr.DoubleField':float,
    'solr.SortableDoubleField':float,
    'solr.DateField':solr_date
    }


def schema_parse(f):
    schemadoc = lxml.etree.parse(f)

    field_types = {}
    for data_type, t in solr_data_types.items():
        for field_type in schemadoc.xpath("/schema/types/fieldType[@class='%s']/@name" % data_type):
            field_types[field_type] = t

    schema_fields = {}
    for field in schemadoc.xpath("/schema/fields/field"):
        schema_fields[field.attrib['name']] = field_types.get(field.attrib['type'], 'UNKNOWN')

    return schema_fields


print schema_parse("/Users/tow/dl/solr/apache-solr-1.3.0/example/solr/conf/schema.xml")