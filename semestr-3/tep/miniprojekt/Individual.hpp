#pragma once

#include <random>
#include <vector>
#include "Evaluator.hpp"

using namespace std;

namespace LcVRPContest
{
    class Individual
    {
    public:
        Individual();
        Individual(const Evaluator* evaluator, int solution_size);
        Individual(const Individual& other);
        Individual& operator=(const Individual& other);
        const vector<int>& GetGenotype() const { return genotype_; }
        void SetGenotype(const vector<int>& genotype) { genotype_ = genotype; }
        double GetFitness() const { return fitness_; }
        void EvaluateFitness();
        void Mutate(double mutation_rate);
        void Crossover(const Individual& other,
                       Individual& offspring1,
                       Individual& offspring2) const;
        void InitializeRandom();
        void SetEvaluator(const Evaluator* evaluator) { evaluator_ = evaluator; }

    private:
        const Evaluator* evaluator_;
        vector<int> genotype_;
        double fitness_;
        int solution_size_;
        static mt19937 random_generator_;
        static bool random_generator_initialized_;
        static void InitializeRandomGenerator();
    };
} // namespace LcVRPContest
