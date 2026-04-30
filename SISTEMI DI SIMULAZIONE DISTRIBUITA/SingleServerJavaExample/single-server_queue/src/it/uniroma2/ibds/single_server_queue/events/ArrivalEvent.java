package it.uniroma2.ibds.single_server_queue.events;

import it.uniroma2.ibds.single_server_queue.application.Event;
import it.uniroma2.ibds.single_server_queue.application.Customer;
import it.uniroma2.ibds.single_server_queue.application.SingleServer;
import it.uniroma2.ibds.single_server_queue.statistics.Statistics;
import it.uniroma2.ibds.single_server_queue.simulation.SimulationExecution;


public class ArrivalEvent extends Event {

    private double serviceTime;

    public ArrivalEvent(double timestamp, double serviceTime) {
        super(timestamp);
        this.serviceTime = serviceTime;
    }

    public double getServiceTime() {
        return serviceTime;
    }
    
    public void setServiceTime(double serviceTime) {
		this.serviceTime = serviceTime;
	}

    @Override
    public void handle(SingleServer server,
                       SimulationExecution execution,
                       Statistics statistics) {

        double now = getTimestamp();

        // ===== update time-based stats =====
        if (server.isBusy()) {

            statistics.areaUnderQ += (now - server.getTimeOfLastEvent())
                    * server.getNumberInQueue();

            statistics.areaUnderB += (now - server.getTimeOfLastEvent());
        }

        server.setTimeOfLastEvent(now);

                // ===== if server idle → start service immediately: a new completion event is scheduled =====
        if (!server.isBusy()) {
            server.setBusy(true);
	    statistics.numberDelayed++;
            double completionTime = now + serviceTime;
            execution.addEvent(
                    completionTime,
                    new CompletionEvent(completionTime)
            );

        } else {
        	//A customer entity is introduced and enqueued
            Customer customer = new Customer(now, serviceTime);
            server.enqueue(customer);
        }
    }
}