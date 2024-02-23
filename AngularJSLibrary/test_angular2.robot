*** Settings ***
Library    SeleniumLibrary
Library    AngularJSLibrary

*** Test Case ***
Open ng2-animations
    Open Browser    https://ng2-animations.firebaseapp.com/
    # Wait For Angular
    # Set Ignore Implicit Angular Wait    ${True}
    Input Text  //app-root//input    Hello
    Click Element  //app-root//button
    Input Text  //app-root//input    World
    Click Element  //app-root//button
    Input Text  //app-root//input    !!!!!
    Click Element  //app-root//button
    Click Element  //app-root//li[2]
    Input Text  //app-root//input    Where did the world go?\t
    Input Text  //app-root//input    Here I am ====> World
    Click Element  //app-root//button
    Sleep  5sec
    Close All Browsers