#include <format>
#include <iostream>
#include "Evaluator.hpp"
#include "GeneticAlgorithm.hpp"
#include "ProblemLoader.hpp"

using namespace LcVRPContest;

void StartOptimization(const string& folder_name,
                       const string& instance_name,
                       int num_groups,
                       int max_iterations)
{
  try
  {
    ProblemLoader problem_loader(folder_name, instance_name);
    ProblemData problem_data = problem_loader.LoadProblem();

    Evaluator evaluator(problem_data, num_groups);

    int population_size = 150;
    float crossover_probability = 0.75;
    float mutation_probability = 0.25;
    GeneticAlgorithm ga(evaluator, population_size, crossover_probability, mutation_probability);

    ga.SetMaxIterations(max_iterations);
    ga.SetMaxTime(3600.0); // 1 hour

    std::string output_filename = instance_name + "_fitness.csv";
    ga.SetOutputFile(output_filename);

    ga.Initialize();

    while (ga.ShouldContinue())
    {
      ga.RunIteration();
    }

    ga.CloseOutputFile();

    const auto& best_solution = ga.GetBestSolution();
    double best_fitness = ga.GetBestFitness();

    std::cout << "=== Optimization Results ===" << std::endl;
    std::cout << "Final best fitness: " << best_fitness << std::endl;
    std::cout << "Iterations completed: " << ga.GetIterationCount() << std::endl;
    std::cout << "Fitness evaluations: " << ga.GetEvaluationCount() << std::endl;
    std::cout << "Elapsed time: " << ga.GetElapsedTime() << " seconds" << std::endl;
    std::cout << "Fitness data saved to: " << output_filename << std::endl;
  }
  catch (const exception& e)
  {
    std::cerr << "Error during optimization: " << e.what() << std::endl;
  }
}

int main()
{
  int num_groups = 21;
  int max_iterations = 1000;

  StartOptimization("Vrp-Set-D", "ORTEC-n323-k21", num_groups, max_iterations);

  return 0;
}
