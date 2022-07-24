*** Settings ***
Suite Setup      Go To Async Page and Wait
Test Setup      Go To Async Page and Wait
Resource        ../resource.robot
Library         AngularJSLibrary

Documentation   This test suite for validating the waiting for angular functionality
...             Based off of protractor\spec\basic\synchronize_spec.js

*** Test Cases ***
Waits For Http Calls
    [Documentation]  `Wait For Angular` should delay for 2 seconds.
    Element Text Should Be  binding=slowHttpStatus  not started
    Click Button  css=[ng-click="slowHttp()"]

    Wait For Angular  timeout=20sec

    Element Text Should Be  binding=slowHttpStatus  done

Implicitly Waits For Http Calls
    [Documentation]  Second `Element Text Should Be` (done) should delay for 2 seconds.
    Element Text Should Be  binding=slowHttpStatus  not started
    Click Button  css=[ng-click="slowHttp()"]
    Element Text Should Be  binding=slowHttpStatus  done

Implicitly Waits For Http Calls (without Binding locators)
    [Documentation]  Second `Element Text Should Be` (done) should delay for 2 seconds.
    Element Text Should Be  css=[ng-bind="slowHttpStatus"]  not started
    Click Button  css=[ng-click="slowHttp()"]
    Element Text Should Be  css=[ng-bind="slowHttpStatus"]  done

Waits For Long Javascript Execution
    [Documentation]  This test will take variable amount of time but should not
    ...    take more than about five seconds.
    Element Text Should Be  binding=slowFunctionStatus  not started
    Click Button  css=[ng-click="slowFunction()"]

    Wait For Angular

    Element Text Should Be  binding=slowFunctionStatus  done

Implicitly Waits For Long Javascript Execution
    [Documentation]  This test will take variable amount of time but should not
    ...    take more than about five seconds.

    Element Text Should Be  css=[ng-bind="slowFunctionStatus"]  not started
    Click Button  css=[ng-click="slowFunction()"]
    Element Text Should Be  css=[ng-bind="slowFunctionStatus"]  done

DOES NOT wait for timeout
    [Documentation]  The `Wait For Angular` keyword should return immediately
    ...    and not wait for a javascript timeout.
    Element Text Should Be  binding=slowTimeoutStatus  not started
    Click Button  css=[ng-click="slowTimeout()"]

    Wait For Angular

    Element Text Should Be  binding=slowTimeoutStatus  pending...

Implicitly DOES NOT wait for timeout
    [Documentation]  The second `Element Text Should Be` keyword (pending...)
    ...    should return immediately and not wait for a javascript timeout.
    Element Text Should Be  css=[ng-bind="slowTimeoutStatus"]  not started
    Click Button  css=[ng-click="slowTimeout()"]
    Element Text Should Be  css=[ng-bind="slowTimeoutStatus"]  pending...

Waits For $timeout
    [Documentation]  `Wait For Angular` should delay for 4 seconds.
    Element Text Should Be  binding=slowAngularTimeoutStatus  not started
    Click Button  css=[ng-click="slowAngularTimeout()"]

    Wait For Angular  timeout=30sec

    Element Text Should Be  binding=slowAngularTimeoutStatus  done
    
Implicitly Waits For $timeout
    [Documentation]  Second `Element Text Should Be` (done) should delay for 4 seconds.
    Element Text Should Be  css=[ng-bind="slowAngularTimeoutStatus"]  not started
    Click Button  css=[ng-click="slowAngularTimeout()"]
    Element Text Should Be  css=[ng-bind="slowAngularTimeoutStatus"]  done
    
Waits For $timeout Then A Promise
    [Documentation]  `Wait For Angular` should delay for around 4 seconds.
    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  not started
    Click Button  css=[ng-click="slowAngularTimeoutPromise()"]

    Wait For Angular  timeout=30sec

    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  done
    
Implicitly Waits For $timeout Then A Promise
    [Documentation]  Second `Element Text Should Be` (done) should delay for around 4 seconds.
    Element Text Should Be  css=[ng-bind="slowAngularTimeoutPromiseStatus"]  not started
    Click Button  css=[ng-click="slowAngularTimeoutPromise()"]
    Element Text Should Be  css=[ng-bind="slowAngularTimeoutPromiseStatus"]  done
    
Waits For Long Http Call Then A Promise
    [Documentation]  `Wait For Angular` should delay for 2 seconds.
    Element Text Should Be  binding=slowHttpPromiseStatus  not started
    Click Button  css=[ng-click="slowHttpPromise()"]

    Wait For Angular  timeout=30sec

    Element Text Should Be  binding=slowHttpPromiseStatus  done

Implicitly Waits For Long Http Call Then A Promise
    [Documentation]  Second `Element Text Should Be` (done) should delay for 2 seconds.
    Element Text Should Be  css=[ng-bind="slowHttpPromiseStatus"]  not started
    Click Button  css=[ng-click="slowHttpPromise()"]
    Element Text Should Be  css=[ng-bind="slowHttpPromiseStatus"]  done

Waits For Slow Routing Changes
    [Documentation]  `Wait For Angular` should delay for around 5 seconds.
    Element Text Should Be  binding=routingChangeStatus  not started
    Click Button  css=[ng-click="routingChange()"]

    Wait For Angular  timeout=30sec

    Page Should Contain  polling mechanism

Implicitly Waits For Slow Routing Changes
    [Documentation]  Second `Element Text Should Be` (done) should delay for around 5 seconds.
    Element Text Should Be  binding=routingChangeStatus  not started
    Click Button  css=[ng-click="routingChange()"]
    Page Should Contain  polling mechanism

Waits For Slow Ng-Include Templates To Load
    [Documentation]  `Wait For Angular` should delay for around 2 seconds.
    Element Text Should Be  css=.included  fast template contents
    Click Button  css=[ng-click="changeTemplateUrl()"]

    Wait For Angular  timeout=30sec
    
    Element Text Should Be  css=.included  slow template contents

Implicitly Waits For Slow Ng-Include Templates To Load
    [Documentation]  Second `Element Text Should Be` (done) should delay for around 2 seconds.
    Element Text Should Be  css=.included  fast template contents
    Click Button  css=[ng-click="changeTemplateUrl()"]
    Element Text Should Be  css=.included  slow template contents

Toggle Implicit Wait For Angular Flag
    Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]

    Set Ignore Implicit Angular Wait  ${true}

    Click Button  css=[ng-click="slowAngularTimeout()"]

    Run Keyword And Expect Error  *  Click Button  css=[ng-click="slowAngularTimeoutHideButton()"]

    Wait For Angular
    Element Should Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]
    Click Element  css=[ng-click="slowAngularTimeoutHideButton()"]
    Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]

    Set Ignore Implicit Angular Wait  ${false}

    Click Button  css=[ng-click="slowAngularTimeout()"]

    Click Button  css=[ng-click="slowAngularTimeoutHideButton()"]

    Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]

*** Keywords ***
Go To Async Page and Wait
    Go To   http://${SERVER}/testapp/ng1/alt_root_index.html#/async
    Wait For Angular