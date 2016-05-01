if [ "$1" = "--rebuild" ]; then echo 'For Help --help' && python getEbayCategories.py; fi
if [ "$1" = "--render" ]; then echo 'For Help --help' && python htmlCategory.py "$2" && open "$2.html"; fi
if [ "$1" = "--help" ]; then echo 'Use command --rebuild to get the information from the ebay API or use the command --render {id} to generate and open the html filed created on the browser'; fi
if [ "$1" != "--rebuild" -a "$1" != "--render" ]; then echo "Command invalid" && echo 'For Help --help'; fi