#include "GeneticAlgorithm.hpp"
#include <algorithm>
#include <climits>
#include <iomanip>
#include <iostream>
#include <limits>

using namespace LcVRPContest;

GeneticAlgorithm::GeneticAlgorithm(Evaluator& evaluator, const int population_size, const double crossover_probability,
                                   const double mutation_probability)
  : population_size_(population_size),
    crossover_probability_(crossover_probability),
    mutation_probability_(mutation_probability),
    max_iterations_(1000),
    max_time_seconds_(3600.0), // 1 hour
    max_evaluations_(INT_MAX),
    evaluator_(evaluator),
    best_fitness_(numeric_limits<double>::lowest()),
    iteration_count_(0),
    evaluation_count_(0),
    rng_(random_device{}())
{
  population_.reserve(population_size_);
}

void GeneticAlgorithm::Initialize()
{
  best_solution_.clear();
  best_solution_.resize(evaluator_.GetSolutionSize());
  best_fitness_ = numeric_limits<double>::lowest();
  iteration_count_ = 0;
  evaluation_count_ = 0;
  population_.clear();
  InitializePopulation();
  EvaluatePopulation();
  UpdateBest();

  start_time_ = chrono::high_resolution_clock::now();

  std::cout << "=== Generation 0 (Initial Population) ===" << std::endl;
  std::cout << "Initial Best Fitness: " << best_fitness_ << std::endl;
  std::cout << "Population Size: " << population_size_ << std::endl;
  LogProgress();
}

void GeneticAlgorithm::RunIteration()
{
  iteration_count_++;

  SelectAndBreed();
  EvaluatePopulation();
  UpdateBest();
  LogProgress();
}

void GeneticAlgorithm::InitializePopulation()
{
  for (int i = 0; i < population_size_; ++i)
  {
    Individual individual(&evaluator_, evaluator_.GetSolutionSize());
    individual.InitializeRandom();
    population_.push_back(individual);
  }
}

void GeneticAlgorithm::EvaluatePopulation()
{
  for (int i = 0; i < static_cast<int>(population_.size()); ++i)
  {
    population_[i].EvaluateFitness();
    evaluation_count_++;
  }
}

void GeneticAlgorithm::SelectAndBreed()
{
  vector<Individual> new_population;
  new_population.reserve(population_size_);

  vector<int> elite_indices;
  elite_indices.reserve(ELITE_SIZE);

  for (int e = 0; e < ELITE_SIZE && e < static_cast<int>(population_.size()); ++e)
  {
    double best_fitness = numeric_limits<double>::lowest();
    int best_idx = 0;

    for (int i = 0; i < static_cast<int>(population_.size()); ++i)
    {
      bool already_selected = false;
      for (int j = 0; j < static_cast<int>(elite_indices.size()); ++j)
      {
        if (elite_indices[j] == i)
        {
          already_selected = true;
          break;
        }
      }

      if (!already_selected && population_[i].GetFitness() > best_fitness)
      {
        best_fitness = population_[i].GetFitness();
        best_idx = i;
      }
    }

    elite_indices.push_back(best_idx);
    new_population.push_back(population_[best_idx]);
  }

  uniform_real_distribution<double> prob_dist(0.0, 1.0);

  while (static_cast<int>(new_population.size()) < population_size_)
  {
    const int parent1_idx = TournamentSelection();
    const int parent2_idx = TournamentSelection();

    Individual offspring1(&evaluator_, evaluator_.GetSolutionSize());
    Individual offspring2(&evaluator_, evaluator_.GetSolutionSize());

    if (prob_dist(rng_) < crossover_probability_)
    {
      population_[parent1_idx].Crossover(population_[parent2_idx], offspring1,
                                         offspring2);
    }
    else
    {
      offspring1 = population_[parent1_idx];
      offspring2 = population_[parent2_idx];
    }

    offspring1.Mutate(mutation_probability_);
    offspring2.Mutate(mutation_probability_);

    new_population.push_back(offspring1);

    if (static_cast<int>(new_population.size()) < population_size_)
    {
      new_population.push_back(offspring2);
    }
  }

  new_population.resize(population_size_);
  population_ = new_population;
}

int GeneticAlgorithm::TournamentSelection()
{
  uniform_int_distribution<int> dist(0, static_cast<int>(population_.size()) - 1);

  int best_idx = dist(rng_);
  double best_fitness = population_[best_idx].GetFitness();

  for (int i = 1; i < TOURNAMENT_SIZE; ++i)
  {
    if (const int candidate_idx = dist(rng_); population_[candidate_idx].GetFitness() > best_fitness)
    {
      best_fitness = population_[candidate_idx].GetFitness();
      best_idx = candidate_idx;
    }
  }

  return best_idx;
}

void GeneticAlgorithm::UpdateBest()
{
  for (int i = 0; i < static_cast<int>(population_.size()); ++i)
  {
    if (population_[i].GetFitness() > best_fitness_)
    {
      best_fitness_ = population_[i].GetFitness();
      best_solution_ = population_[i].GetGenotype();
    }
  }
}

bool GeneticAlgorithm::ShouldContinue() const
{
  if (iteration_count_ >= max_iterations_)
  {
    return false;
  }

  if (GetElapsedTime() >= max_time_seconds_)
  {
    return false;
  }

  if (evaluation_count_ >= max_evaluations_)
  {
    return false;
  }

  return true;
}

double GeneticAlgorithm::GetElapsedTime() const
{
  const auto end_time = chrono::high_resolution_clock::now();
  const chrono::duration<double> elapsed = end_time - start_time_;
  return elapsed.count();
}

void GeneticAlgorithm::SetOutputFile(const string& filename)
{
  if (output_file_.is_open())
  {
    output_file_.close();
  }
  output_file_.open(filename);
  if (output_file_.is_open())
  {
    output_file_ << "iteration,fitness,evaluations,time\n";
  }
}

void GeneticAlgorithm::CloseOutputFile()
{
  if (output_file_.is_open())
  {
    output_file_.close();
  }
}

void GeneticAlgorithm::LogProgress()
{
  if (iteration_count_ % 10 == 0)
  {
    std::cout << "Generation " << iteration_count_ << ": Best Fitness: " << best_fitness_ << ", Evaluations: " <<
      evaluation_count_ << ", Time: " << std::fixed << std::setprecision(2) << GetElapsedTime() << "s" << std::endl;
  }

  if (output_file_.is_open())
  {
    output_file_ << iteration_count_ << "," << best_fitness_ << ","
      << evaluation_count_ << "," << GetElapsedTime() << "\n";
    output_file_.flush();
  }
}
