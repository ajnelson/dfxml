check: \
  check-dfxml \
  check-cat_fileobjects \
  check-dfxml_tool \
  check-idifference-dfxml \
  check-mac_timelines
	@echo "Tests passed!"

check-dfxml:
	./test_dfxml.sh

check-cat_fileobjects:
	./test_cat_fileobjects.sh

check-dfxml_tool:
	./test_dfxml_tool.sh

check-idifference-dfxml:
	./test_idifference_to_dfxml.sh

check-mac_timelines:
	./test_mac_timelines.sh
	
clean:
	rm -f dfxml_tool_*xml
	rm -f cat_test_{,no}cache.dfxml
	rm -f idifference_test.txt
	rm -f idifference_test{,_formatted}.dfxml
	rm -f demo_mac_timeline*.txt

check-validate: \
  ../deps/dfxml_schema/dfxml.xsd \
  ../schema/delta.xsd \
  idifference_test_formatted.dfxml
	xmllint --noout --schema ../schema/delta.xsd idifference_test_formatted.dfxml
	xmllint --noout --schema ../deps/dfxml_schema/dfxml.xsd idifference_test_formatted.dfxml
#The second command fails unless the extension elements are laxly validated (processContents="lax" instead of "strict")

idifference_test_formatted.dfxml: test_idifference_to_dfxml.sh
	./test_idifference_to_dfxml.sh

../deps/dfxml_schema/dfxml.xsd:
	pushd .. ; \
	  git submodule init deps/dfxml_schema ; \
	  git submodule update deps/dfxml_schema ; \
	  popd
