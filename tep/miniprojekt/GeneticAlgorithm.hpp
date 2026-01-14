#pragma once

#include "Evaluator.hpp"
#include "Individual.hpp"

#include <chrono>
#include <fstream>
#include <random>
#include <vector>

using namespace std;

namespace LcVRPContest
{
  class GeneticAlgorithm
  {
  public:
    explicit GeneticAlgorithm(Evaluator& evaluator, int population_size = 150, double crossover_probability = 0.75,
                              double mutation_probability = 0.25);
    void Initialize();
    void RunIteration();
    void SetMaxIterations(const int max_iterations) { max_iterations_ = max_iterations; }
    void SetMaxTime(const double max_time_seconds) { max_time_seconds_ = max_time_seconds; }
    void SetMaxEvaluations(const int max_evaluations) { max_evaluations_ = max_evaluations; }
    bool ShouldContinue() const;
    const vector<int>& GetBestSolution() const { return best_solution_; }
    double GetBestFitness() const { return best_fitness_; }
    int GetIterationCount() const { return iteration_count_; }
    int GetEvaluationCount() const { return evaluation_count_; }
    double GetElapsedTime() const;
    void SetOutputFile(const string& filename);
    void CloseOutputFile();

  private:
    int population_size_;
    double crossover_probability_;
    double mutation_probability_;

    int max_iterations_;
    double max_time_seconds_;
    int max_evaluations_;

    Evaluator& evaluator_;
    vector<Individual> population_;
    vector<int> best_solution_;
    double best_fitness_;
    int iteration_count_;
    int evaluation_count_;

    mt19937 rng_;

    ofstream output_file_;
    chrono::high_resolution_clock::time_point start_time_;

    static constexpr int TOURNAMENT_SIZE = 3;
    static constexpr int ELITE_SIZE = 5;

    void InitializePopulation();
    void EvaluatePopulation();
    void SelectAndBreed();
    int TournamentSelection();
    void UpdateBest();
    void LogProgress();
  };
} // namespace LcVRPContest
