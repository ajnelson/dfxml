all: check-validate

check-validate:
	xmllint --noout --schema ../deps/dfxml_schema/dfxml.xsd ../samples/difference_test_0.xml
	xmllint --noout --schema ../deps/dfxml_schema/dfxml.xsd ../samples/difference_test_1.xml
