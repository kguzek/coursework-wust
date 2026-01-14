#include "Evaluator.hpp"
#include "Optimizer.hpp"
#include "ProblemLoader.hpp"
#include <iostream>

using namespace LcVRPContest;

void StartOptimization(const string& folder_name, const string& instance_name, int num_groups, int max_iterations)
{
    ProblemLoader problem_loader(folder_name, instance_name);
    ProblemData problem_data = problem_loader.LoadProblem();

    Evaluator evaluator(problem_data, num_groups);
    Optimizer optimizer(evaluator);

    optimizer.Initialize();

    for (int i = 0; i < max_iterations; ++i)
    {
        optimizer.RunIteration();
    }

    vector<int>* best_solution = optimizer.GetCurrentBest();
    double best_fitness = evaluator.Evaluate(*best_solution);
    cout << "final best fitness: " << best_fitness << endl;
}

int main()
{
    int num_groups = 21;
    int max_iterations = 10;

    StartOptimization("Vrp-Set-D", "ORTEC-n323-k21", num_groups, max_iterations);

    return 0;
}
