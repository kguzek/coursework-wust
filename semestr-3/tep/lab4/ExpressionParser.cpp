#include <iostream>
#include <map>
#include <sstream>
#include <string>

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
        "6. equals <drzewo>  \t porównuje podane wyrażenie ze stanem wgranego drzewa" << std::endl <<
        "7. quit             \t kończy działanie programu" << std::endl <<
        "8. help             \t wyświetla tą wiadomość" << std::endl << std::endl <<
        "wiersze zaczynające się znakiem '#' będą ignorowane." << std::endl;
}

std::string get_first_error_message(const std::vector<Error*>& errors)
{
    return errors.front()->get_message();
}

int main()
{
    Result<ExpressionTree*, Error> tree = new Error("nie wprowadzono drzewa");
    std::string line;
    while (std::getline(std::cin, line) && line != "quit")
    {
        int first_word_end;
        for (first_word_end = 0; first_word_end < line.length() && line[first_word_end] != ' '; first_word_end++)
        {
        }
        std::string command = line.substr(0, first_word_end);
        std::string argument = line.substr(first_word_end);
        if (command.empty() || command[0] == '#')
        {
        }
        else if (command == "enter")
        {
            if (tree.is_success())
            {
                delete tree.get_value();
            }
            tree = ExpressionTree::parse(argument);
            if (!tree.is_success())
            {
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
                tree = new Error("poprzednio wpisane drzewo zawierało błędy");
            }
        }
        else if (command == "vars")
        {
            if (tree.is_success())
            {
                std::set<std::string> seen_variables;
                tree.get_value()->get_root()->print_variable_children(std::cout, seen_variables);
                std::cout << std::endl;
            }
            else
            {
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
            }
        }
        else if (command == "print")
        {
            if (tree.is_success())
            {
                std::cout << *tree.get_value() << std::endl;
            }
            else
            {
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
            }
        }
        else if (command == "comp")
        {
            if (tree.is_success())
            {
                std::stringstream variable_names;
                std::set<std::string> seen_variables;
                tree.get_value()->get_root()->print_variable_children(variable_names, seen_variables);

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
                    std::cout << tree.get_value()->get_root()->calculate_value(variables_map) << std::endl;
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
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
            }
        }
        else if (command == "join")
        {
            if (tree.is_success())
            {
                Result<ExpressionTree*, Error> joined_tree = ExpressionTree::parse(argument);
                if (joined_tree.is_success())
                {
                    *tree.get_value() = *tree.get_value() + *joined_tree.get_value();
                    delete joined_tree.get_value();
                }
                else
                {
                    std::cerr << get_first_error_message(joined_tree.get_errors()) << std::endl;
                }
            }
            else
            {
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
            }
        }
        else if (command == "equals")
        {
            if (tree.is_success())
            {
                Result<ExpressionTree*, Error> target_tree = ExpressionTree::parse(argument);
                if (target_tree.is_success())
                {
                    bool equal = *tree.get_value() == *target_tree.get_value();
                    std::cout << (equal ? "true" : "false") << std::endl;
                    delete target_tree.get_value();
                }
                else
                {
                    std::cerr << get_first_error_message(target_tree.get_errors()) << std::endl;
                }
            }
            else
            {
                std::cerr << get_first_error_message(tree.get_errors()) << std::endl;
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
    if (tree.is_success()) {
        delete tree.get_value();
    }
}
