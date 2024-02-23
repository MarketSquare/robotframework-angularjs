*** Settings ***
Library    SeleniumLibrary
Library    AngularJSLibrary    root_selector=material-docs-app

*** Test Cases ***
Add Favorite Animal To Dialog
    Open Browser  https://material.angular.io/cdk/dialog/examples  Chrome
    Input Text    //input[@for='dialog-user-name']  Robot Framework
    Click Button  Pick one
    Input Text    //input[@for='favorite-animal']  Aibo
    Click Button  OK
    Element Text Should Be    //cdk-dialog-overview-example/ol/li[3]    You chose: Aibo