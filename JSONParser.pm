package Local::JSONParser;

use strict;
use warnings;
use base qw(Exporter);
our @EXPORT_OK = qw( parse_json );
our @EXPORT = qw( parse_json );

use Encode;
use utf8;

my $JSON = qr{

    (?(DEFINE)

        (?<value>
            \s*(
                (?&string)
                |(?&number)
                |(?&object)
                |(?&array)
                |true (?{ [$^R, 1] })
                |false (?{ [$^R, 0] })
                |null (?{ [$^R, undef] })
                |(?&incorrect)
            )\s*
        )

        (?<string>
            "(
                (
                    \\[\\"\/bfnrt]
                    |\\u[0-9a-fA-F]{4}
                    |[\w\s\d+:\{\}\[\],@-]
                )*
            )"
            (?{
                [
                    $^R,
                    eval {
                        local $_ = $^N;
                        s/(?<!\\)\\u([0-9A-Fa-f]{4})/pack 'U*',hex($1)/eg;
                        s/(?<!\\)(\\r)/chr(13)/eg;
                        s/(?<!\\)(\\f)/chr(12)/eg;
                        s/(?<!\\)(\\n)/chr(10)/eg;
                        s/(?<!\\)(\\t)/chr(9)/eg;
                        s/(?<!\\)(\\b)/chr(8)/eg;
                        s/\\\//\//g;
                        s/\\\\/\\/g;
                        s/\\"/"/g;
                        return $_;
                    }
                ] 
            })
        )

        (?<number>
            (-?
                (?:
                    0
                    |[1-9]\d*
                )
                (?:
                    \.\d+
                )?
                (?:
                    [eE][+-]?\d+
                )?
            ) 
            (?{ [$^R, $^N] })
        )

        (?<object>
            (?{ [$^R, {}] })
            \{\s*
                (?: 
                    (?&key_value)
                    (?{
                        [
                            $^R->[0][0],
                            {$^R->[1] => $^R->[2]}
                        ]
                    })
                    (?:
                        \s*,\s*
                        (?&key_value)
                        (?{
                            $^R->[0][1]{ $^R->[1] } = $^R->[2];
                            $^R->[0]
                        })
                    )*
                )?
            \s*\}
        )

        (?<array>
            (?{ [$^R, [] ] })
            \[\s*
                (?:
                    (?&value)
                    (?{
                        [$^R->[0][0],
                        [$^R->[1]]]
                    })
                    (?:
                        \s*,\s*
                        (?&value)
                        (?{
                            push @{$^R->[0][1]}, $^R->[1];
                            $^R->[0]
                        })
                    )*
                )?
            \s*\]
        )

        (?<incorrect>
            ^(.+)$
            (?{
                die "Incorrect JSON: $^N\n"
            })
        )

        (?<key_value>
            (?&string)
            \s*:\s*
            (?&value) 
            (?{
                [$^R->[0][0],
                $^R->[0][1],
                $^R->[1]]
            })
        )

    )

    ^(?&value)$ (?{ $_ = $^R->[1] })

}xms;

sub parse_json {
    local $_ = decode('utf-8', shift);
    /^$JSON$/;
    return $_;
}

1;
