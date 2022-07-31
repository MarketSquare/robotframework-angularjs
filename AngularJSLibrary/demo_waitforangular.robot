*** Settings ***
Library    SeleniumLibrary
Library    AngularJSLibrary    ignore_implicit_angular_wait=True

*** Test Cases ***
Search Through The Phone Catalog For Samsung Phones
    Open Browser  http://angular.github.io/angular-phonecat/step-14/app  Chrome
    Wait For Angular
    Input Text  //input  Samsung
    Wait For Angular
    Click Link  Samsung Galaxy Tab™
    Wait For Angular
    Element Text Should Be    css:phone-detail h1    Samsung Galaxy Tab™