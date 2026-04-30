package it.uniroma2.ibds.single_server_queue.simulation;

import java.util.Arrays;
import java.util.List;
import java.util.TreeMap;

import it.uniroma2.ibds.single_server_queue.application.Event;
import it.uniroma2.ibds.single_server_queue.application.SingleServer;
import it.uniroma2.ibds.single_server_queue.events.ArrivalEvent;
import it.uniroma2.ibds.single_server_queue.statistics.Statistics;

public class SimulationExecution {

	private double now = 0.0; //simulation time
	private TreeMap<Double, Event> eventList = new TreeMap<Double, Event>();
	
	SingleServer singleServerInstance;
	Statistics statistics;
	
	List<Double> interarrivalTimes = Arrays.asList(0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9);
	List<Double> serviceTimes = Arrays.asList(2.0, 0.7, 0.2, 1.1, 3.7, 0.6);
	
	int numberDelayed;
	
	public double getSimulationTime() {
		return now;
	}
	
	public void setSimulationTime (double currentTime) {
		now = currentTime;
	}
	
	public void addEvent(double timeStamp, Event e) {
		eventList.put(timeStamp,e);
	}
	
	public SimulationExecution() {

		singleServerInstance = new SingleServer();
		statistics = new Statistics();

		double arrivalTimestamp = 0;
		// Insert of interarrival times in the pending event list
		for (int i = 0; i < interarrivalTimes.size(); i++) {
			arrivalTimestamp += interarrivalTimes.get(i);
			double serviceTime = (i < serviceTimes.size())
					? serviceTimes.get(i)
					: Double.POSITIVE_INFINITY;
			//loop.getPendingEventList().put(arrivalTimestamp, new ArrivalEvent(arrivalTimestamp, serviceTime));
			eventList.put(arrivalTimestamp, new ArrivalEvent(arrivalTimestamp, serviceTime));
		}
	}
	public void run() {

		// Number of delayed after that we stop simulation
		numberDelayed = 6;

		// Run simulation until numberDelayed is not 6
		while (statistics.numberDelayed < numberDelayed) {
			
			Event e = (Event) eventList.remove(eventList.firstKey());
			
			now = e.getTimestamp();
			e.handle(singleServerInstance, this, statistics);

			// Print results for the current event:
			System.out.printf("******************** %s with timestamp: %.1f ********************\n", e.getClass().getSimpleName(),
					e.getTimestamp());
			//System.out.println(singleServerInstance);
			singleServerInstance.printServerStatus();
			System.out.printf("\tClock: %.1f \n", now);
			System.out.println(statistics);
		}

		// Final report

		System.out.println("******************** Final output performance measures: ********************");
		System.out.println(
				String.format("\t Average delay in queue: %.2f min./cust.",
						statistics.totalDelay / numberDelayed));
		System.out.println(
				String.format("\t Time-average number in queue: %.2f custs.",
						statistics.areaUnderQ / now));
		System.out
				.println(String.format("\t Server utilization: %.2f",
						statistics.areaUnderB / now));
	}

}
