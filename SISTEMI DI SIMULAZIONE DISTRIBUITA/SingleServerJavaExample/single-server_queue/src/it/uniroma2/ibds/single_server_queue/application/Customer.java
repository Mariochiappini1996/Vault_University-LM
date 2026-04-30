package it.uniroma2.ibds.single_server_queue.application;

public class Customer {

    private final double arrivalTime;
    private final double serviceTime;

    public Customer(double arrivalTime, double serviceTime) {
        this.arrivalTime = arrivalTime;
        this.serviceTime = serviceTime;
    }

    public double getArrivalTime() {
        return arrivalTime;
    }

    public double getServiceTime() {
        return serviceTime;
    }
}
