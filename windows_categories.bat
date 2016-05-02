ECHO OFF
CLS
ECHO.

if "%1"=="--rebuild" (
    ECHO 'For Help --help' && py getEbayCategories.py
)

if "%1"=="--render" (
    ECHO 'For Help --help' && py htmlCategory.py "%2" && "%2.html"
)

if "%1"=="--help" (
    ECHO "Use command --rebuild to get the information from the ebay API or use the command --render {id} to generate and open the html filed created on the browser"
)

if not "%1" == "--rebuild" if not "%1" == "--render" if not "%1" == "--help" (
    ECHO "Command invalid" && ECHO "For Help --help"
)