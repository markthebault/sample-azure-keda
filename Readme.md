# Keda and Azure with Service bus example

You need to modify the `keda-msi.yaml` to use your MSI (look azure pod idenity if you don't know what it is)
and then change the repository URL in `Makefile` to use yours.

then edit the `queue-reader-func.yaml` to update the Servicebus namespace and queue used by the app

Then you can run `make all` to run the examples, you will have to publics message to the service bus by yourself or use a datalake event.

to remove everything that was created, just run `make destroy`