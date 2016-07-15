use strict;

sub getTemplate($) {
	my $wikitext = shift;
	$wikitext =~ /(\{\{coord.*?\}\})/i;
	$1;
}

sub determineType($) {
	my $coords = shift;
	if ($coords !~ /\|[NS]\|/) {
		return 0;
	} elsif ($coords =~ /^([^\|]*?\|){1}[^|]*\|[NS]\|/i) {
		return 1;
	} elsif ($coords =~ /^([^\|]*?\|){2}[^|]*\|[NS]\|/i) {
		return 2;
	} elsif ($coords =~ /^([^\|]*?\|){3}[^|]*\|[NS]\|/i) {
		return 3;
	}
}

sub printDegrees($$$$) {
	my ($lat, $latHS, $lng, $lngHS) = (shift, shift, shift, shift);
	if ($latHS == 'N') {
		print "$lat ";
	} else {
		print "-$lat ";
	}
	if ($lngHS == 'W') {
		print "$lng\n";
	} else {
		print "-$lng\n";
	}
}

my $wikitext;
{
	local $/;
	$wikitext = <>;
}


if ($wikitext =~ /{{coord missing/i) {
	exit;
}

my $coords = getTemplate $wikitext;
my $type = determineType $coords;

my @coords = split /\|/, $coords;

if ($type == 0) {
	print "$coords[1] $coords[2]\n";
} elsif ($type == 1) {
	printDegrees $coords[1], $coords[2], $coords[3], $coords[4];
} elsif ($type == 2) {
	$coords[1] += $coords[2] / 60;
	$coords[4] += $coords[5] / 60;
	printDegrees $coords[1], $coords[3], $coords[4], $coords[6];
} elsif ($type == 3) {
	$coords[1] += $coords[2] / 60 + $coords[3] / 3600;
	$coords[5] += $coords[6] / 60 + $coords[7] / 3600;
	printDegrees $coords[1], $coords[4], $coords[5], $coords[8];
}
