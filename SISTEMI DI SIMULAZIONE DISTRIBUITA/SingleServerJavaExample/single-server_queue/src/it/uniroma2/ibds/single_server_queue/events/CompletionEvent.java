package it.uniroma2.ibds.single_server_queue.events;

import it.uniroma2.ibds.single_server_queue.application.Event;
import it.uniroma2.ibds.single_server_queue.application.Customer;
import it.uniroma2.ibds.single_server_queue.application.SingleServer;
import it.uniroma2.ibds.single_server_queue.statistics.Statistics;
import it.uniroma2.ibds.single_server_queue.simulation.SimulationExecution;

public class CompletionEvent extends Event {

    public CompletionEvent(double timestamp) {
        super(timestamp);
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

        server.setBusy(false); //service completed, server is now idle

        // ===== start next customer if exists =====
        if (server.hasWaitingCustomers()) {
        	/*
        	 * If there are customers in the queue, the first one is served: 
        	 * a corresponding completion new event is scheduled.
        	 * */
            Customer next = server.dequeue();
            server.setBusy(true); 
            double completionTime = now + next.getServiceTime();
            statistics.numberDelayed++;
            statistics.totalDelay += now - next.getArrivalTime();
            execution.addEvent(
                    completionTime,
                    new CompletionEvent(completionTime)
            );
        }
    }
}