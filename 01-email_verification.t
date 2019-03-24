#!/usr/bin/env perl

use Modern::Perl;
use Test::More;
use FindBin;
use lib "$FindBin::Bin/../lib";
use Local::ValidationEmail qw(email_verification);

sub test_email_verification($$) {
my ($address, $expected) = @_;
	my $got;

	eval {
		$got = email_verification($address);
	1} or do {
		fail "test( $address )";
		diag "Упал из-за $@";
		return;
	};

	my $ok = 0;
    CHECK: {
		last if $got ne $expected;
		$ok = 1;
	}

	if (!$ok) {
		fail "test( $address )";
		diag "Вернул: ",explain $got;
		diag "Ожидается: ",explain $expected;
	} else {
		pass "test( $address )";
	}

}

test_email_verification 'info@mail.ru', 'mail.ru';
test_email_verification 'support@vk.com', 'vk.com';
test_email_verification 'ddd@rambler.ru', 'rambler.ru';
test_email_verification 'roxette@mail.ru', 'mail.ru';
test_email_verification 'example@localhost', 'localhost';
test_email_verification 'иван@иванов.рф', 'иванов.рф';
test_email_verification 'ivan@xn--c1ad6a.xn--p1ai', 'xn--c1ad6a.xn--p1ai';
test_email_verification 'sdfsdf@@@@@rdfdf', '';

test_email_verification 'simple@example.com', 'example.com';
test_email_verification 'very.common@example.com', 'example.com';
test_email_verification 'disposable.style.email.with+symbol@example.com', 'example.com';
test_email_verification 'other.email-with-hyphen@example.com', 'example.com';
test_email_verification 'fully-qualified-domain@example.com', 'example.com';
test_email_verification 'user.name+tag+sorting@example.com', 'example.com';
test_email_verification 'x@example.com', 'example.com';
test_email_verification 'example-indeed@strange-example.com', 'strange-example.com';
test_email_verification 'admin@mailserver1', 'mailserver1';
test_email_verification 'example@s.example', 's.example';
test_email_verification '" "@example.org', 'example.org';
test_email_verification '"john..doe"@example.org', 'example.org';

test_email_verification 'Abc.example.com', '';
test_email_verification 'A@b@c@example.com', '';
test_email_verification 'a"b(c)d,e:f;g<h>i[j\k]l@example.com', '';
test_email_verification 'just"not"right@example.com', '';
test_email_verification 'this is"not\allowed@example.com', '';
test_email_verification 'this\ still\"not\\allowed@example.com', '';
test_email_verification '1234567890123456789012345678901234567890123456789012345678901234+x@example.com', '';
test_email_verification '', '';

done_testing();
