*** Settings ***
Documentation     A test suite with a single test for valid login.

Library           SeleniumLibrary

*** Variables ***
${SERVER}         localhost:8000
${BROWSER}        Chrome
${DELAY}          0
${VALID USER}     robot_tester
${VALID PASSWORD}    robot_tester
${HOME URL}       ${SERVER}/
${LOGIN URL}      ${SERVER}/login/

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Login | Nordism

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username_field    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password_field    ${password}

Submit Credentials
    Click Button    login_button

Home Page Should Be Open
    Location Should Be    ${Home URL}
    Title Should Be    Home | Nordism

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    ${VALID USER}
    Input Password    ${VALID PASSWORD}
    Submit Credentials
    Home Page Should Be Open
    [Teardown]    Close Browser