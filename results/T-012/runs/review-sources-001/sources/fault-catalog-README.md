# fault_replicate


## Fault Replication Branches list (22): You can check the fault replication details on following branches of this git repository. For more details, please reference https://fudanselab.github.io/research/MSFaultEmpiricalStudy/

### F1: ts-error-process-seq-F1
#### Industrial fault description:
F1 is a fault that occurs in using asynchronous tasks in a single request, when we send messages asynchronously without message sequence control.
Suppose we have Event A and Event B in a request, while Event A always processes and returns earlier than Event B.
But sometimes, due to some specific reasons, Event A processes and returns later than Event B.
Then F1 will occur.
#### TrainTicket replicated fault description:
In ticket-cancellation logic of the TrainTicket system, we have two major events: [Drawback Money] and [Reset Order Status].
If the user decided to cancel an order, the Ticket-Cancel-Service firstly call Inside-Payment-Service to drawback money.
Then Inside-Payment-Service call Order-Service to set the order status to CANCELLING. 
Then the system refunds the money to user.
After that, the Cancel-Service call Order-Service set the order status to CANCEL. 
Then the whole cancel process is done.
In our fault reproduction, we made a random delay in event [Drawback Money] to simulate the situation of network congestion.
In this case, the event [Reset Order Stauts] will complete before [Drawback Money], then the fault occurs.


### F2: ts-error-reportui-F2
#### Industrial fault description:
F2 is a fault that multiple messages are displayed in wrong order.
Sometimes we send many requests at a short time.
However, these requests may returns at a different order with the origin.
If we display the information without checking the order of these requests, wrong information may be shown on the screen.
Then this kind of fault occurs.
#### TrainTicket replicated fault description:
In TrainTicket system, every request for ticket-reservation has a random delay to simulate the unstable network condition.
If a user send multiple requests for ticket-reservation at a short time, the order of the result may be wrong due to the random delay.
Then this fault occurs.


### F3: ts-error-docker-JVM-F3
#### Industrial fault description:
F3 is a fault which occurs when the microservice is not properly configured.
If a micorservice is implemented by Java and using Docker as container, JVM and Docker configuration is needed.
However, JVM and Docker both have same configuration such as memory limit and cpu limit, while configuration in JVM and configuration in Docker influences each other.
If these configuration is not properly set, the microservice will have some unexpected behavior.
#### TrainTicket replicated fault description:
In the reproduction of F3, we mis-configured some microservice such that the JVM memory limit is bigger than the Docker memory limit.
In this case, if the requests occupy too much memory, the JVM process will be killed, leading to the microservices unavailable periodly.
Then the fault occurs.


### F4: ts-error-ssl-F4
#### Industrial fault description:
F4 is fault of SSL offloading which leads to the response time for some requests is very long.
#### TrainTicket replicated fault description:
In TrainTicket system, we apply SSL to every microservice.
When we send requests about some complex logic, we will find that the response time is very long.
In this scenario, the faults occurs.

### F5: ts-error-cross-timeout-status(chance)-F5
#### Industrial fault description:
F5 is such kind of fault which is caused by the resource competition of multiple requests.
Sometimes a microservice has its maximum number of connections by using thread pool.
Suppose we have 3 services, A, B, C. A and B both call C for some specific information.
If A send some requests to C, but before that B has sent some requests to C and these requests are too complex to process at a short time, then
the requests from A must wait until the requests from B completed, leading to a timeout exception.
#### TrainTicket replicated fault description:
We implemented this fault in Basic-Info-Service. 
We use asynchronous tasks in Basic-Info-Service to collect tickets information.
Then we use the thread pool which is needed for the implementation of asynchronous tasks as microservice resource.
We send many requests at a short period of time and if the thread number is equal or exceeds the max-thread-pool-size, the fault will occur.

### F6: ts-error-F6
#### Industrial fault description:
A service is slowing down and returns error finally.
Endless recursive requests of a microservice are caused by SQL errors of another dependent microservice.
#### TrainTicket replicated fault description:
In out train ticket system, we replicate this fault in voucher service.
The SQL arg in voucher service is something wrong, make the request fail.
When the request is fail, the host service will send another request.
After many retries, we will receive a timeout error finally.

### F7: ts-external-normal-F7
#### Industrial fault description:
F7 is a fault which occurs in a third-party service and then leads to a failure.
We always need to call a microservice that maintained by a third-party or company.
Sometimes the response from the microservice maintained by others may be timeout and returns nothing, or even return wrong information.
Then this kind of fault occurs.
#### TainTicket replicated fault description:
In TainTicket system, if the user want to buy a ticket but the balance is not enough, the system will call a third-party service implemented by Node.js to get the ticket money. 
Sometimes there will be a delay in this third-party service, then the timeout will be triggered and the fault occurs.

### F8: ts-error-redis-F8
#### Industrial fault description:
This fault is caused by the error of redis in the operation of getting the saved key/token.
The microservice always save some key/token to redis.
However, sometimes the developer may made a mistake and the program may be mis-implemented.
In such case, the key/token may be wrongly read and deliver a missing/wrong key/token to other microservice, leading to an fault.
#### TrainTicket replicated fault description:
We have two types of users in TrainTicket system: normal user and VIP user.
Compared to the normal user, the VIP user has one more key/token to be used in ticket-booking process.
However, when vip user is processing ticket-reservation logic, the key/token is missing when delivering.
Then the fault occurs.


### F9: ts-error-F9
#### Industrial fault description:
There is a Right To Left (RTL) display error for UI words.
There is a CSS display style error in bi-directional.
#### TrainTicket replicated fault description:
Fault occurs when convert from LTR to RTL in Login Block.

### F10: ts-error-logic-F10
#### Industrial fault description:
F10 is caused by an unexpected output of a microservice, which is used in a special case of business processing.
#### train_ticket replicated fault description:
We replicate this fault in ticket reservation process.
In contacts service we have two APIs serve for the ticket reservation process in different situation. 
Sometimes in a specific situation that is not correctly handled, these APIs may be wrongly invoded, thus making the ticket reservation process fail.   


### F11: ts-error-bomupdate-F11
#### Industrial fault description:
F11 is a fault due to the lack of sequence control.
Note that such a fault may not always occur, making  it difficult to analyze.
Sometimes if a return value is too far from the normal value, the microsevice will recheck the correctness of the value and correct it.
But this process does not always happen, making the result sometimes wrong but sometimes right.
#### TrainTicket replicated fault description:
In TrainTicket system, there are two microservices set the same value in the database in order cancellation process.
Due to the lack of control like F1, the two microservices may set the value in a wrong sequence.
However, the second microservice that set the value may recheck the value and correct the value.
The recheck process does not always happen.
If two microservices set the value in a wrong sequence but the recheck process does not executed, this fault occurs.

### F12: ts-error-processes-seq-status(chance)-F12-Final
#### Industrial fault description:
F12 is one kind of faults that occurs due to the specific status of some microservice.
The word "status" has a wide range of meanings, for example, a global value in one microservice.
If a microservice is in some specific "status", the fault occurs.
This kind of faults only occurs in some specific status of a microservice.
Because the fault only occurs in specific status, when we analyze the root cause of the microservice, we must combine the microservice status.
#### TrainTicket replicated fault description:
We have two specific status in Order-Service: locked station and thread-pool size.
If the admin is operating the orders between two stations, such two stations will be added to the locked station list.
And the thread-pool is used for Order-Service to do some asynchronous tasks.
If the user want to cancel a order whose start station or terminal station is in the locked station list, the request will be rejected.
Then the fault occurs.

### F13: ts-error-queue-F13
#### Industrial fault description:
F13 is one kind of fault due to the wrong processing order of multiple requests.
In a complex business process, we need send many requests in order to complete our business.
However, if we send these requests in a short period of time(eg. fast click), these reqeusts may not be processed in order due to the transmission delay or some other reason.
If the latter request needs the result of the previous request, such kind of fault like F13 will occur.
#### TrainTicket replicated fault description:
In TrainTicket system, if a user want to complete a ticket-booking process and a ticket-cancellation process, he/she will send many requests.
These reqeusts includes login, searching for tickets, selecting contacts, confirming tickets, payment and comfirming cancellation.
All these requests have a random delay to simulate the process delay.
If the comfirming cancellation is already begun but the payment process is still not completed yet, this fault will occur.

### F14: ts-error-F14
#### Industrial fault description:
The result of the Consumer Price Index (CPI) is wrong.
There is a mistake in including the locked product in CPI calculation.
#### TrainTicket replicated fault description:
In our Train Ticket system, we replicate this fault in ticket price calculating.
When calculating the second class seat price, the calculating process is wrong, leading to a fault.

### F15: ts-error-F15
#### Industrial fault description:
The data-synchronization job quits unexpectedly.
The spark actor is used for the configuration of actorSystem (part of Apache Spark) instead of the system actor.
#### TrainTicket replicated fault description:
Limit the post json size to 200 bytes in nginx.conf file.
If user select the food and consign, the request body will exceed 200 bytes, and the request will be blocked by nginx.

### F16: ts-error-F16
#### Industrial fault description:
The file-uploading process fails.
The "max-content-length" configuration of spray is only 2 Mb, not allowing to support to upload a big file.
#### TrainTicket replicated fault description:
Our system has the ability to add routes in batches. You can upload the file to add routes in batches.
But the size of the permitted file is too small, sometimes your file will be rejected because of the size.

### F17: ts-error-F17
#### Industrial fault description:
The grid-loading process takes too much time.
Too many nested "select" and "from" clauses are in the constructed SQL statement.
#### TrainTicket replicated fault description:
To simulate the nested select clauses, one procedure of mysql to sleep 10s was created in ts-voucher-service.
Since the front stage has a 5s limit of network request, the query of one order's voucher will be out of time.

### F18: ts-error-F18
#### Industrial fault description:
Loading the product-analysis chart is erroneous.
One key of the returned JSON data for the UI chart includes the null value.
#### TrainTicket replicated fault description:
When user select a train which doesn't have train food, the return result of 'getFood' will be null.
But the front stage should get the first item which represents trainfood of the result without check whether it's null.

### F19: ts-error-F19
#### Industrial fault description:
The price is displayed in an unexpectedly format.
The product price is not formatted correctly in the French format.
#### TrainTicket replicated fault description:
When the user chooses to consign his packages and select the French format, the returned price is displayed in wrong format.
The product price is not formatted correctly in the French format.
### F20: ts-error-F20
#### Industrial fault description:
Nothing is returned upon workflow data request.
The JBoss startup classpath parameter does not include the right DB2 jar package.
#### TrainTicket replicated fault description:
Many microservices share a same lib. This lib contains some basic data structure such as Enum of Order status.
The value of same order status in different version is in different value.
If some microservice use an old version lib but some use a new version lib, the fault will occur.

### F21: ts-error-F21
#### Industrial fault description:
JAWS (a screen reader) misses reading some elements.
The "aria-labeled-by" element for accessibility cannot be located by the JAWS.
#### TrainTicket replicated fault description:
Just add the aria label in the login module.
There are three input types to read - Email, Password and Verification Code.
When the cursor focuses on the input, the screen reader will read the value in it.
Add the "aria-labelledby" label to the "Email" and "Password" inputs to first read the input name,
so that user can make clear what the input value represent.
But the "Verification Code" input doesn't add an "aria-labelledby" label
So user will just heard the input's default value "abcd", it will confuse the user.

### F22: ts-error-F22
#### Industrial fault description:
The error of SQL column missing is returned upon some data request.
The constructed SQL statement includes a wrong column name in the "select" part according to its "from" part
#### TrainTicket replicated fault description:
The constructed SQL statement includes a wrong column name in the "select" part according to its "from" part.
When the user switch to Flow Three - Consign & Voucher and click the button of "Print Voucher" if any, the result page displays "Empty. No data!".
