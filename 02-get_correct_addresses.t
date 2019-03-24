#!/usr/bin/env perl

use Modern::Perl;
use Test::More;
use Test::Deep::NoTest;
use FindBin;
use lib "$FindBin::Bin/../lib";
use Local::ValidationEmail qw(get_correct_addresses);

sub test_get_correct_addresses($) {
    my $file = shift;
    my $got_one;
    my $got_two;

    eval {
        ($got_one, $got_two) = get_correct_addresses($file);
    1} or do {
        fail "test( $file )";
        diag "Упал из-за $@";
        return;
    };

    my $expected_one = {
        'example.com' => 7,
        'example.org' => 2,
        'localhost' => 1,
        'mail.ru' => 2,
        'mailserver1' => 1,
        'rambler.ru' => 1,
        's.example' => 1,
        'strange-example.com' => 1,
        'vk.com' => 1,
        'xn--c1ad6a.xn--p1ai' => 1
    };
    my $expected_two = 8;

    my $ok = 0;
    CHECK: {
        last if !eq_deeply($got_one, $expected_one);
        last if $expected_two != $$got_two;
        $ok = 1;
    };

    if (!$ok) {
        fail "test( $file )";
        diag "Вернул: ",explain $got_one;
        diag "Ожидается: ",explain $expected_one;
    } else {
        pass "test( $file )";
    }

}

sub test_bad_get_correct_addresses($) {
    my $file = shift;
    my $got;

    eval {
        $got = get_correct_addresses($file);
    1} or do {
        pass "test( $file )";
        return;
    };

    fail "tets( $file )";
    diag "Должен был упасть, но вернул: ", explain $got;

}

test_get_correct_addresses 'example.txt';

test_bad_get_correct_addresses 'example_1.txt';
test_bad_get_correct_addresses 'example_2.txt';
test_bad_get_correct_addresses 'example_3.txt';
test_bad_get_correct_addresses '';

done_testing();
