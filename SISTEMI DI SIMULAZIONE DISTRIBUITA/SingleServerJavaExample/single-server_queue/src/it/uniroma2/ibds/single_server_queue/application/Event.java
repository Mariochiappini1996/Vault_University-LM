package it.uniroma2.ibds.single_server_queue.application;

import it.uniroma2.ibds.single_server_queue.statistics.Statistics;
import it.uniroma2.ibds.single_server_queue.simulation.SimulationExecution;

public abstract class Event {
	
	private double timestamp;
	
	public Event(double timestamp) {
		this.timestamp = timestamp;
	}

	public double getTimestamp() {
		return timestamp;
	}

	public abstract void handle(SingleServer sys, SimulationExecution execution, Statistics statistics);
	
}
