*** Settings ***
Test Setup      Go To   http://${SERVER}/testapp/ng1/alt_root_index.html#/async
Resource        ../resource.robot
Library         AngularJSLibrary

*** Test Cases ***
Waits For Http Calls
    Wait For Angular
    Element Text Should Be  binding=slowHttpStatus  not started

    Click Button  ng-click=slowHttp()

    Wait For Angular  timeout=20sec
    Element Text Should Be  binding=slowHttpStatus  done

Waits For Long Javascript Execution
    Wait For Angular
    Element Text Should Be  binding=slowFunctionStatus  not started

    Click Button  ng-click=slowFunction()

    Wait For Angular
    Element Text Should Be  binding=slowFunctionStatus  done

DOES NOT wait for timeout
    Wait For Angular
    Element Text Should Be  binding=slowTimeoutStatus  not started

    Click Button  ng-click=slowTimeout()

    Wait For Angular
    Element Text Should Be  binding=slowTimeoutStatus  pending...

Waits For $timeout
    Wait For Angular
    Element Text Should Be  binding=slowAngularTimeoutStatus  not started

    Click Button  ng-click=slowAngularTimeout()

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowAngularTimeoutStatus  done
    
Waits For $timeout Then A Promise
    Wait For Angular
    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  not started

    Click Button  ng-click=slowAngularTimeoutPromise()

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  done
    
Waits For Long Http Call Then A Promise
    Wait For Angular
    Element Text Should Be  binding=slowHttpPromiseStatus  not started

    Click Button  ng-click=slowHttpPromise()

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowHttpPromiseStatus  done

Waits For Slow Routing Changes
    Wait For Angular
    Element Text Should Be  binding=routingChangeStatus  not started

    Click Button  ng-click=routingChange()

    Wait For Angular  timeout=30sec
    Page Should Contain  polling mechanism

Waits For Slow Ng-Include Templates To Load
    Wait For Angular
    Element Text Should Be  css=.included  fast template contents

    Click Button  ng-click=changeTemplateUrl()

    Wait For Angular  timeout=30sec
    Element Text Should Be  css=.included  slow template contents

Wait Times Out
    Wait For Angular
    Element Text Should Be  binding=slowAngularTimeoutStatus  not started

    Click Button  ng-click=slowAngularTimeout()

    Run Keyword And Expect Error  *  Wait For Angular  timeout=1sec

Log Pending Http Calls
    Wait For Angular
    Element Text Should Be  binding=slowHttpPromiseStatus  not started

    Click Button  ng-click=slowHttpPromise()

    Run Keyword And Expect Error  *  Wait For Angular  timeout=1sec

Implicit Wait For Angular On Timeout
    Wait For Angular

    Click Button  ng-click=slowAngularTimeout()

    Click Button  ng-click=slowAngularTimeoutHideButton()

Implicit Wait For Angular On Timeout With Promise
    Wait For Angular

    Click Button  ng-click=slowAngularTimeoutPromise()

    Click Button  ng-click=slowAngularTimeoutPromiseHideButton()

Toggle Implicit Wait For Angular Flag
    Element Should Not Be Visible  ng-click=slowAngularTimeoutHideButton()

    Set Ignore Implicit Angular Wait  ${true}

    Click Button  ng-click=slowAngularTimeout()

    Run Keyword And Expect Error  *  Click Button  ng-click=slowAngularTimeoutHideButton()

    Wait For Angular
    Element Should Be Visible  ng-click=slowAngularTimeoutHideButton()
    Click Element  ng-click=slowAngularTimeoutHideButton()
    Element Should Not Be Visible  ng-click=slowAngularTimeoutHideButton()

    Set Ignore Implicit Angular Wait  ${false}

    Click Button  ng-click=slowAngularTimeout()

    Click Button  ng-click=slowAngularTimeoutHideButton()

    Element Should Not Be Visible  ng-click=slowAngularTimeoutHideButton()