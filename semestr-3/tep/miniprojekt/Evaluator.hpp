#pragma once

#include "ProblemData.hpp"
#include <vector>

using namespace std;

namespace LcVRPContest
{
    class Evaluator
    {
    public:
        Evaluator(const ProblemData& problem_data, int num_groups);

        double Evaluate(const vector<int>* solution) const;
        double Evaluate(const vector<int>& solution) const;
        double Evaluate(const int* solution) const;

        int GetSolutionSize() const { return num_customers_; }
        static int GetLowerBound() { return 0; }
        int GetUpperBound() const { return num_groups_ - 1; }
        int GetNumGroups() const { return num_groups_; }

        const ProblemData& GetProblemData() const { return problem_data_; }

    private:
        const ProblemData& problem_data_;
        int num_groups_;
        int num_customers_;

        const double WRONG_VAL = -1.0;
        const double PENALTY_INVALID_SOLUTION = -1000000.0;

        double CalculateRouteCost(const vector<int>& route) const;
        bool IsValidSolution(const vector<int>& grouping) const;
        bool ValidateConstraints() const;
        void BuildRoutes(const vector<int>& grouping, vector<vector<int>>& routes) const;

        bool CheckCapacityConstraint(const vector<int>& route) const;
        bool CheckDistanceConstraint(const vector<int>& route) const;
        double CalculateRouteDemand(const vector<int>& route) const;
        double CalculateTotalDistance(const vector<int>& route) const;
        bool IsValidCustomerIndex(int customer_id) const;
    };
}
