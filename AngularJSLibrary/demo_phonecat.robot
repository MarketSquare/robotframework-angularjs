*** Settings ***
Library    SeleniumLibrary
Library    AngularJSLibrary    root_selector=[ng-app]

*** Test Cases ***
Search Through The Phone Catalog For Samsung Phones
    Open Browser  http://angular.github.io/angular-phonecat/step-14/app  Chrome
    Input Text  //input  Samsung
    Click Link  Samsung Galaxy Tab™
    Element Text Should Be    css:phone-detail h1    Samsung Galaxy Tab™