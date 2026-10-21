import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.regex.Pattern;

/** Exemplo autocontido de ordenacao topologica deterministica. */
public final class DependencyPlanner {
    private static final Pattern SAFE_ID = Pattern.compile("[A-Za-z0-9][A-Za-z0-9._-]*");
    private final Map<String, Set<String>> prerequisites = new HashMap<>();
    private final Map<String, Set<String>> dependents = new HashMap<>();

    private static void validateTask(String task) {
        if (task == null || !SAFE_ID.matcher(task).matches()) {
            throw new IllegalArgumentException("identificador deve usar apenas ASCII seguro");
        }
    }

    public void addTask(String task) {
        validateTask(task);
        prerequisites.computeIfAbsent(task, ignored -> new HashSet<>());
        dependents.computeIfAbsent(task, ignored -> new HashSet<>());
    }

    public void addDependency(String task, String prerequisite) {
        validateTask(task);
        validateTask(prerequisite);
        addTask(task);
        addTask(prerequisite);
        prerequisites.get(task).add(prerequisite);
        dependents.get(prerequisite).add(task);
    }

    public List<String> topologicalOrder() {
        Map<String, Integer> indegree = new HashMap<>();
        prerequisites.forEach((task, required) -> indegree.put(task, required.size()));

        PriorityQueue<String> ready = new PriorityQueue<>();
        indegree.forEach((task, degree) -> {
            if (degree == 0) {
                ready.add(task);
            }
        });

        List<String> result = new ArrayList<>();
        while (!ready.isEmpty()) {
            String task = ready.remove();
            result.add(task);
            for (String dependent : dependents.get(task)) {
                int degree = indegree.merge(dependent, -1, Integer::sum);
                if (degree == 0) {
                    ready.add(dependent);
                }
            }
        }

        if (result.size() != prerequisites.size()) {
            List<String> blocked = new ArrayList<>();
            indegree.forEach((task, degree) -> {
                if (degree > 0) {
                    blocked.add(task);
                }
            });
            blocked.sort(String::compareTo);
            throw new IllegalStateException("ciclo detectado entre: " + blocked);
        }
        return List.copyOf(result);
    }

    private static void requireBefore(Collection<String> order, String first, String second) {
        List<String> values = new ArrayList<>(order);
        if (values.indexOf(first) >= values.indexOf(second)) {
            throw new AssertionError(first + " deveria vir antes de " + second);
        }
    }

    public static void main(String[] args) {
        DependencyPlanner planner = new DependencyPlanner();
        planner.addDependency("api", "modelo");
        planner.addDependency("testes", "api");
        planner.addDependency("release", "testes");
        planner.addDependency("release", "docs");
        List<String> order = planner.topologicalOrder();
        requireBefore(order, "modelo", "api");
        requireBefore(order, "api", "testes");
        requireBefore(order, "testes", "release");
        System.out.println(String.join(" -> ", order));

        DependencyPlanner invalid = new DependencyPlanner();
        try {
            invalid.addDependency("api", " modelo");
            throw new AssertionError("o identificador invalido deveria ser rejeitado");
        } catch (IllegalArgumentException expected) {
            if (!invalid.topologicalOrder().isEmpty()) {
                throw new AssertionError("a operacao invalida nao pode mutar o grafo");
            }
        }

        DependencyPlanner cyclic = new DependencyPlanner();
        cyclic.addDependency("A", "B");
        cyclic.addDependency("B", "A");
        try {
            cyclic.topologicalOrder();
            throw new AssertionError("o ciclo deveria ser rejeitado");
        } catch (IllegalStateException expected) {
            System.out.println(expected.getMessage());
        }
    }
}
