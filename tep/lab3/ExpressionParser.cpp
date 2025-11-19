#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

#include "ExpressionTree.h"

void output_help()
{
    std::cout <<
        "dostępne komendy:" << std::endl <<
        "1. enter <wyrażenie>\t wczytuje wyrażenie algebraiczne do drzewa" << std::endl <<
        "2. vars             \t wypisuje wszystkie zmienne we wczytanym wyrażeniu" << std::endl <<
        "3. print            \t wypisuje stan drzewa w notacji polskiej" << std::endl <<
        "4. comp <wartości>  \t oblicza wyrażenie wstawiając pod zmienne podane wartości" << std::endl <<
        "5. join <wyrażenie> \t tworzy nowe drzewo i łączy je do poprzedniego" << std::endl <<
        "6. quit             \t kończy działanie programu" << std::endl <<
        "7. help             \t wyświetla tą wiadomość" << std::endl;
}

int main()
{
    ExpressionTree* tree;
    std::string line;
    bool tree_initialized = false;
    while (std::getline(std::cin, line) && line != "quit")
    {
        int first_word_end;
        for (first_word_end = 0; first_word_end < line.length() && line[first_word_end] != ' '; first_word_end++)
        {
        }
        std::string command = line.substr(0, first_word_end);
        std::string argument = line.substr(first_word_end);
        if (command.empty())
        {
        }
        else if (command == "enter")
        {
            if (tree_initialized)
            {
                delete tree;
            }
            tree = new ExpressionTree(argument);
            tree_initialized = true;
        }
        else if (command == "vars")
        {
            if (tree_initialized)
            {
                std::set<std::string> seen_variables;
                tree->get_root()->print_variable_children(std::cout, seen_variables);
                std::cout << std::endl;
            }
            else
            {
                std::cerr << "nie można wypisać zmiennych przed wprowadzeniem wyrażenia" << std::endl;
            }
        }
        else if (command == "print")
        {
            if (tree_initialized)
            {
                std::cout << *tree << std::endl;
            }
            else
            {
                std::cerr << "nie można wypisać drzewa przed wprowadzeniem wyrażenia" << std::endl;
            }
        }
        else if (command == "comp")
        {
            if (tree_initialized)
            {
                std::stringstream variable_names;
                std::set<std::string> seen_variables;
                tree->get_root()->print_variable_children(variable_names, seen_variables);

                int key_count = 0;
                int value_count = 0;
                std::string temp;

                std::stringstream key_counter(variable_names.str());
                while (key_counter >> temp)
                {
                    ++key_count;
                }

                std::istringstream value_counter(argument);
                while (value_counter >> temp)
                {
                    ++value_count;
                }

                if (key_count == value_count)
                {
                    std::map<std::string, int> variables_map;
                    std::stringstream key_stream(variable_names.str());
                    std::istringstream value_stream(argument);

                    std::string key;
                    std::string value_str;
                    while (key_stream >> key && value_stream >> value_str)
                    {
                        std::istringstream iss(value_str);
                        int value;
                        if (!(iss >> value))
                        {
                            value = DEFAULT_CONSTANT_VALUE;
                            std::cerr <<
                                "niepoprawna wartość zmiennej: " << value_str << std::endl <<
                                "użyto domyślnej wartości:     " << value << std::endl;
                        }
                        variables_map[key] = value;
                    }
                    std::cout << tree->get_root()->calculate_value(variables_map) << std::endl;
                }
                else
                {
                    std::cerr <<
                        "niepoprawna ilość wartości zmiennych: oczekiwano " <<
                        key_count << "; otrzymano " << value_count << std::endl;
                }
            }
            else
            {
                std::cerr << "nie można obliczyć wartości wyrażenia przed jego wprowadzeniem" << std::endl;
            }
        }
        else if (command == "join")
        {
            if (tree_initialized)
            {
                const ExpressionTree joined_tree(argument);
                *tree = *tree + joined_tree;
            }
            else
            {
                std::cerr << "nie można dołączyć do drzewa przed wprowadzeniem wyrażenia" << std::endl;
            }
        }
        else if (command == "help")
        {
            output_help();
        }
        else
        {
            std::cerr <<
                "nieznana komenda: '" << command << "'" << std::endl <<
                "wpisz 'help', aby otrzymać listę dostępnych komend" << std::endl;
        }
    }
}
