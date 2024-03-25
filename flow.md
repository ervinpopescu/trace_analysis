# Execution flow

In each trace file, do the following tasks:
  - If a request is successful, then determine:
    - Policies that are invoked and policies that are skipped
    - If there are any shared flows, flow hooks
    - The backend server to which the request was sent
    - Response from backend server
    - Final response sent to the client
    - Variables read or assigned from different policies
  - If a request is failed, then determine
    - The failing response code
    - The cause of the failure
    - Message ID for the failed request
    - Fault Code, Fault Source from AX phase
    - Error Message
  - If the issue is caused by Apigee, Customer’s Policy Code or Customer’s Backend Server
  - Root cause of the issue
  - Any other unique observations from the Trace Files
