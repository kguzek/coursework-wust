# Systemy Operacyjne — Laboratoria

## Zadanie 5 — Kolejkowanie Zadań przy Wielu Procesorach

- próg wykorzystania procesora — np. 80%
- losowanie procesora aż wylosowany będzie nieobciążony
- maksymalna liczba losowań (`z`)
- gdy dokonano `z` losowań, a procesor nie jest go w stanie obsłużyć (np. wykorzystanie 99% przy 5% wymaganej mocy
  obliczeniowej) to proces czeka aż się któryś zwolni

### Przykładowe wartości

```py
p_high: float = 0.8  # 80%
z: int = 5
```
