package it.uniroma2.ibds.single_server_queue.application;

import java.util.LinkedList;
import java.util.Queue;

public class SingleServer {

    private boolean serverBusy;
    private int numberInQueue;

    private Queue<Customer> queue; 	//entity customer is introduced

    private double timeOfLastEvent;

    public SingleServer() {
        this.serverBusy = false;	//false = idle, true = busy
        this.numberInQueue = 0;
        this.queue = new LinkedList<>();
        this.timeOfLastEvent = 0.0;
    }

    public boolean isBusy() {
        return serverBusy;
    }

    public void setBusy(boolean serverBusy) {
        this.serverBusy = serverBusy;
    }

    public int getNumberInQueue() {
        return numberInQueue;
    }

    public double getTimeOfLastEvent() {
        return timeOfLastEvent;
    }

    public void setTimeOfLastEvent(double timeOfLastEvent) {
        this.timeOfLastEvent = timeOfLastEvent;
    }

    public void enqueue(Customer c) {
        queue.add(c);
        numberInQueue++;
    }

    public Customer dequeue() {
        if (queue.isEmpty()) return null;
        numberInQueue--;
        return queue.poll();
    }

    public boolean hasWaitingCustomers() {
        return !queue.isEmpty();
    }

    public Queue<Customer> getQueue() {
        return queue;
    }
    
    public void printServerStatus() {

        System.out.println("\tServer busy: " + this.serverBusy +
                "\n\tNumber in queue: " + this.numberInQueue);

        System.out.println("\n\tCustomer Queue:");

        int i = 1;
        for (Customer c : this.queue) {
            System.out.format(
                    "\t\t%d) arrival=%.1f service=%.1f\n",
                    i++,
                    c.getArrivalTime(),
                    c.getServiceTime()
            );
        }

        System.out.format(
                "\n\tTime of last event: %.1f\n",
                this.timeOfLastEvent
        );
    }
}