#include "Individual.hpp"
#include <algorithm>
#include <random>

using namespace LcVRPContest;

mt19937 Individual::random_generator_;
bool Individual::random_generator_initialized_ = false;

void Individual::InitializeRandomGenerator()
{
  if (!random_generator_initialized_)
  {
    random_device rd;
    random_generator_.seed(rd());
    random_generator_initialized_ = true;
  }
}

Individual::Individual()
  : evaluator_(nullptr), fitness_(0.0), solution_size_(0)
{
}

Individual::Individual(const Evaluator* evaluator, const int solution_size)
  : evaluator_(evaluator), fitness_(0.0), solution_size_(solution_size)
{
  genotype_.resize(solution_size);
  InitializeRandomGenerator();
}

Individual::Individual(const Individual& other)
  : evaluator_(other.evaluator_),
    genotype_(other.genotype_),
    fitness_(other.fitness_),
    solution_size_(other.solution_size_)
{
}

Individual& Individual::operator=(const Individual& other)
{
  if (this != &other)
  {
    evaluator_ = other.evaluator_;
    genotype_ = other.genotype_;
    fitness_ = other.fitness_;
    solution_size_ = other.solution_size_;
  }
  return *this;
}

void Individual::InitializeRandom()
{
  if (evaluator_ == nullptr)
  {
    return;
  }

  InitializeRandomGenerator();
  uniform_int_distribution dist(Evaluator::GetLowerBound(), evaluator_->GetUpperBound());

  for (int i = 0; i < solution_size_; ++i)
  {
    genotype_[i] = dist(random_generator_);
  }
}

void Individual::EvaluateFitness()
{
  if (evaluator_ == nullptr)
  {
    fitness_ = 0.0;
    return;
  }
  fitness_ = evaluator_->Evaluate(genotype_);
}

void Individual::Mutate(const double mutation_rate)
{
  if (evaluator_ == nullptr)
  {
    return;
  }

  InitializeRandomGenerator();
  uniform_real_distribution prob_dist(0.0, 1.0);
  uniform_int_distribution value_dist(Evaluator::GetLowerBound(), evaluator_->GetUpperBound());

  for (int i = 0; i < solution_size_; ++i)
  {
    if (prob_dist(random_generator_) < mutation_rate)
    {
      genotype_[i] = value_dist(random_generator_);
    }
  }
}

void Individual::Crossover(const Individual& other, Individual& offspring1, Individual& offspring2) const
{
  if (evaluator_ == nullptr)
  {
    return;
  }

  InitializeRandomGenerator();
  uniform_int_distribution crossover_point_dist(1, solution_size_ - 1);

  const int crossover_point = crossover_point_dist(random_generator_);

  offspring1.genotype_.assign(genotype_.begin(), genotype_.begin() + crossover_point);
  offspring1.genotype_.insert(offspring1.genotype_.end(), other.genotype_.begin() + crossover_point,
                              other.genotype_.end());

  offspring2.genotype_.assign(other.genotype_.begin(), other.genotype_.begin() + crossover_point);
  offspring2.genotype_.insert(offspring2.genotype_.end(), genotype_.begin() + crossover_point,
                              genotype_.end());
}
