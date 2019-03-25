package Local::Calc;

use 5.010;
use strict;
use warnings;
BEGIN{
    if ($] < 5.018) {
        package experimental;
        use warnings::register;
    }
}
no warnings 'experimental';

use Exporter 'import';
our @EXPORT_OK = qw(tokenize rpn evaluate);

# description of operators
my $operators = {
    'U-' => {
        'priority' => 4,
        'association' => 'right',
        'arguments' => 1,
        'action' => sub { -$_[0] }
    },
    'U+' => {
        'priority' => 4,
        'association' => 'right',
        'arguments' => 1,
        'action' => sub { $_[0] }
    },
    '^' => {
        'priority' => 3,
        'association' => 'right',
        'arguments' => 2,
        'action' => sub { $_[1] ** $_[0] }
    },
    '*' => {
        'priority' => 2,
        'association' => 'left',
        'arguments' => 2,
        'action' => sub { $_[1] * $_[0] }
    },
    '/' => {
        'priority' => 2,
        'association' => 'left',
        'arguments' => 2,
        'action' => sub { $_[1] / $_[0] }
    },
    '-' => {
        'priority' => 1,
        'association' => 'left',
        'arguments' => 2,
        'action' => sub { $_[1] - $_[0] }
    },
    '+' => {
        'priority' => 1,
        'association' => 'left',
        'arguments' => 2,
        'action' => sub { $_[1] + $_[0] }
    }
};

# check function 'string is an integer'
sub is_int {
    my $num = shift;
    if ($num =~ /^\d+$/) {
        return 1;
    }
}

# check function 'string is float'
sub is_float {
    my $num = shift;
    if ($num =~ /^\d*\.\d+$/) {
        return 1;
    }
}

# check function 'string is an exponetial'
sub is_exp {
    my $num = shift;
    if ($num =~ /^\d+e[-+]?\d+|\d*\.\d+e[-+]?\d+$/) {
        return 1;
    }
}

=head1 DESCRIPTION

Эта функция должна принять на вход арифметическое выражение,
а на выходе дать ссылку на массив, состоящий из отдельных токенов.
Токен - это отдельная логическая часть выражения: число, скобка или арифметическая операция
В случае ошибки в выражении функция должна вызывать die с сообщением об ошибке

Знаки '-' и '+' в первой позиции, или после другой арифметической операции стоит воспринимать
как унарные и можно записывать как "U-" и "U+"

Стоит заметить, что после унарного оператора нельзя использовать бинарные операторы
Например последовательность 1 + - / 2 невалидна. Бинарный оператор / идёт после использования унарного "-"

=cut

sub tokenize {
    chomp(my $expr = shift);
    # split by operators and numbers
    my @tokens = split m{([-+^*/)(]|\d*\.?\d*e+[+-]*\d+|\d*\.*\d*\.*\d*)}, $expr;
    # filtering by probes and empty lines
    @tokens = grep !m|^\s*$|, @tokens;
    # for a string of unit length
    if (
        $#tokens == 0
        && !is_int($tokens[0])
        && !is_float($tokens[0])
        && !is_exp($tokens[0])
    ) {
        die "Bad: '$tokens[0]'";
    }
    # for a string not of unit length
    for (my $i = 0; $i < scalar @tokens; $i++) {
        # checking for unknown characters
        if (
            !is_int($tokens[$i])
            && !is_float($tokens[$i])
            && !is_exp($tokens[$i])
            && $tokens[$i] ne ')'
            && $tokens[$i] ne '('
            && !exists $operators->{$tokens[$i]}
        ) {
            die "Bad: '$tokens[$i]'";
        }
        # translate numbers in the correct format
        if ( is_float($tokens[$i]) ) {
            $tokens[$i] += 0;
        }
        elsif ( is_exp($tokens[$i]) ) {
            $tokens[$i] += 0;
        }
        # for 'U+' and 'U-'
        if (
            $tokens[$i] eq '+'
            && (
                $tokens[$i - 1] =~ m{^[-+(*/^]|U-|U+$}
                || $i == 0
            )
        ) {
            $tokens[$i] = 'U+';
        }
        elsif (
            $tokens[$i] eq '-'
            && (
                $tokens[$i - 1] =~ m{^[-+(*/^]|U-|U+$}
                || $i == 0
            )
        ) {
            $tokens[$i] = 'U-';
        }
        # for exeption operators
        if (
            $i == $#tokens
            && $tokens[$i] =~ m{^[-+(*/^]|U-|U+$}
        ) {
            die "Bad: '$tokens[$i - 1]$tokens[$i]'";
        }
        elsif (
            $tokens[$i] =~ m{^[*/^]$}
            && $tokens[$i - 1] =~ m{^[-+(*/^]|U-|U+$}
        ) {
            die "Bad: '$tokens[$i - 1]$tokens[$i]'";
        }
        elsif (
            $tokens[$i] eq ')'
            && $tokens[$i - 1] =~ m{^[-+(*/^]$}
        ) {
            die "Bad: '$tokens[$i - 1]$tokens[$i]'";
        }
        elsif (
            $i > 0
            && (
                is_int($tokens[$i])
                || is_float($tokens[$i])
                || is_exp($tokens[$i])
            )
            && (
                is_int($tokens[$i - 1])
                || is_float($tokens[$i - 1])
                || is_exp($tokens[$i - 1])
            )
        ) {
            die "Bad: '$tokens[$i - 1]$tokens[$i]'";
        }
    }
    return \@tokens;
}

=head1 DESCRIPTION

Эта функция должна принять на вход арифметическое выражение,
а на выходе дать ссылку на массив, содержащий обратную польскую нотацию
Один элемент массива - это число или арифметическая операция
В случае ошибки функция должна вызывать die с сообщением об ошибке

=cut

sub rpn {
    my $expr = shift;
    my $tokens = tokenize($expr);
    my @queue;
    # translation into reverse polish notation
    my @stack;
    for my $char (@{$tokens}) {
        # if the token is a number, then add it to the output queue
        if (
            is_int($char)
            || is_float($char)
            || is_exp($char)
        ) {
            push @queue, $char;
        }
        # if the token is an operator
        elsif ( exists $operators->{$char} ) {
            while (my $last = pop @stack) {
                # while at the top of the stack there is a token operator $last, as well as the operator $char
                # left-associative and its priority is less or the same as the $last operator, or the char 
                # operator is right-associative and its priority is less than that of the $last operator
                if (
                    exists $operators->{$last}
                    && $operators->{$char}->{'association'} eq 'left'
                    && $operators->{$char}->{'priority'} <= $operators->{$last}->{'priority'}
                ) {
                    push @queue, $last;
                } else {
                    push @stack, $last;
                    last;
                }
            }
            push @stack, $char;
        }
        # if the token is a left parenthesis, then put it on the stack
        elsif ( $char eq '(' ) {
            push @stack, $char;
        }
        # if the token is a right parenthesis, then put it on the stack
        elsif ( $char eq ')' ) {
            # before appearing on the top of the token stack "left round bracket"
            # move operators from the stack to the output queue
            while (my $last = pop @stack) {
                ($last eq '(') ? last : push @queue, $last;
            }
        }
    }
    # when there are no tokens left on the input
    # if tokens remain on the stack
    while (my $last = pop (@stack)) {
        push @queue, $last;
    }
    return \@queue;
}

=head1 DESCRIPTION

Эта функция должна принять на вход ссылку на массив, который представляет из себя обратную польскую нотацию,
а на выходе вернуть вычисленное выражение

=cut

sub evaluate {
    my $rpn = shift;
    # solve
    my @stack;
    my @result;
    for my $char (@{$rpn}) {
        if ( !exists $operators->{$char} ) {
            push @result, $char;
        }
        else {
            if ( $operators->{$char}->{'arguments'} == 1 ) {
                push @result, $operators->{$char}->{'action'}->( pop @result );
            } else {
                push @result, $operators->{$char}->{'action'}->( pop @result, pop @result );
            }
            pop @stack;
        }
    }
    return $result[0];
}

1;
