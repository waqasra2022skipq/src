#---------------------------------------------------------------------------#
#          Copyright (c) 1997-2010 PDFlib GmbH. All rights reserved.        #
#---------------------------------------------------------------------------#
#    This software may not be copied or distributed except as expressly     #
#    authorized by PDFlib GmbH's general license agreement or a custom      #
#    license agreement signed by PDFlib GmbH.                               #
#    For more information about licensing please refer to www.pdflib.com.   #
#---------------------------------------------------------------------------#

#
#---------------------------------------------------------------------------*
#              PDFlib - A library for generating PDF on the fly             |
#---------------------------------------------------------------------------+

package PDFlib::PDFlib;

use strict;
use Carp;
use warnings::register;

use pdflib_pl 9.2;
our $VERSION = 9.2;

sub new {
    my $class = shift;
    my $self = {};
    my $pdf = PDF_new();

    bless $self, $class;
    $self->{pdf} = $pdf;
    PDF_set_parameter($pdf, "objorient", "true");

    return $self;
}

sub DESTROY {
    my $self = shift;

    PDF_delete($self->{pdf}) if $self->{pdf};
}

# Automatically generated methods


sub activate_item {
    my $self = shift;
    eval {
	PDF_activate_item($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub add_nameddest {
    my $self = shift;
    eval {
	PDF_add_nameddest($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub add_path_point {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_add_path_point($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub add_portfolio_file {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_add_portfolio_file($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub add_portfolio_folder {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_add_portfolio_folder($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub add_table_cell {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_add_table_cell($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub add_textflow {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_add_textflow($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub add_thumbnail {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_add_thumbnail(): Deprecated");
        }
	PDF_add_thumbnail($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub align {
    my $self = shift;
    eval {
	PDF_align($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub arc {
    my $self = shift;
    eval {
	PDF_arc($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub arcn {
    my $self = shift;
    eval {
	PDF_arcn($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_document {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_begin_document($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub begin_dpart {
    my $self = shift;
    eval {
	PDF_begin_dpart($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_font {
    my $self = shift;
    eval {
	PDF_begin_font($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_glyph {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_begin_glyph(): Deprecated, use PDF_begin_glyph_ext()");
        }
	PDF_begin_glyph($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_glyph_ext {
    my $self = shift;
    eval {
	PDF_begin_glyph_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_item {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_begin_item($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub begin_layer {
    my $self = shift;
    eval {
	PDF_begin_layer($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_mc {
    my $self = shift;
    eval {
	PDF_begin_mc($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_page_ext {
    my $self = shift;
    eval {
	PDF_begin_page_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub begin_pattern {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_begin_pattern(): Deprecated, use PDF_begin_pattern_ext()");
        }
	$ret = PDF_begin_pattern($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub begin_pattern_ext {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_begin_pattern_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub begin_template {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_begin_template(): Deprecated, use PDF_begin_template_ext()");
        }
	$ret = PDF_begin_template($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub begin_template_ext {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_begin_template_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub circle {
    my $self = shift;
    eval {
	PDF_circle($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub circular_arc {
    my $self = shift;
    eval {
	PDF_circular_arc($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub clip {
    my $self = shift;
    eval {
	PDF_clip($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_font {
    my $self = shift;
    eval {
	PDF_close_font($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_graphics {
    my $self = shift;
    eval {
	PDF_close_graphics($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_image {
    my $self = shift;
    eval {
	PDF_close_image($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_pdi {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_close_pdi(): Deprecated, use PDF_close_pdi_document()");
        }
	PDF_close_pdi($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_pdi_document {
    my $self = shift;
    eval {
	PDF_close_pdi_document($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub close_pdi_page {
    my $self = shift;
    eval {
	PDF_close_pdi_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub closepath {
    my $self = shift;
    eval {
	PDF_closepath($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub closepath_fill_stroke {
    my $self = shift;
    eval {
	PDF_closepath_fill_stroke($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub closepath_stroke {
    my $self = shift;
    eval {
	PDF_closepath_stroke($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub concat {
    my $self = shift;
    eval {
	PDF_concat($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub continue_text {
    my $self = shift;
    eval {
	PDF_continue_text($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub convert_to_unicode {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_convert_to_unicode($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_3dview {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_3dview($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_action {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_action($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_annotation {
    my $self = shift;
    eval {
	PDF_create_annotation($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub create_devicen {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_devicen($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_bookmark {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_bookmark($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_field {
    my $self = shift;
    eval {
	PDF_create_field($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub create_fieldgroup {
    my $self = shift;
    eval {
	PDF_create_fieldgroup($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub create_gstate {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_gstate($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub create_pvf {
    my $self = shift;
    eval {
	PDF_create_pvf($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub create_textflow {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_create_textflow($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub curveto {
    my $self = shift;
    eval {
	PDF_curveto($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub define_layer {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_define_layer($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub delete_path {
    my $self = shift;
    eval {
	PDF_delete_path($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub delete_pvf {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_delete_pvf($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub delete_table {
    my $self = shift;
    eval {
	PDF_delete_table($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub delete_textflow {
    my $self = shift;
    eval {
	PDF_delete_textflow($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub draw_path {
    my $self = shift;
    eval {
	PDF_draw_path($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub ellipse {
    my $self = shift;
    eval {
	PDF_ellipse($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub elliptical_arc {
    my $self = shift;
    eval {
	PDF_elliptical_arc($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub encoding_set_char {
    my $self = shift;
    eval {
	PDF_encoding_set_char($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_document {
    my $self = shift;
    eval {
	PDF_end_document($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_dpart {
    my $self = shift;
    eval {
	PDF_end_dpart($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_font {
    my $self = shift;
    eval {
	PDF_end_font($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_glyph {
    my $self = shift;
    eval {
	PDF_end_glyph($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_item {
    my $self = shift;
    eval {
	PDF_end_item($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_layer {
    my $self = shift;
    eval {
	PDF_end_layer($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_mc {
    my $self = shift;
    eval {
	PDF_end_mc($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_page_ext {
    my $self = shift;
    eval {
	PDF_end_page_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_pattern {
    my $self = shift;
    eval {
	PDF_end_pattern($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_template {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_end_template(): Deprecated, use PDF_end_template_ext()");
        }
	PDF_end_template($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub end_template_ext {
    my $self = shift;
    eval {
	PDF_end_template_ext($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub endpath {
    my $self = shift;
    eval {
	PDF_endpath($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fill {
    my $self = shift;
    eval {
	PDF_fill($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fill_graphicsblock {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fill_graphicsblock($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fill_imageblock {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fill_imageblock($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fill_pdfblock {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fill_pdfblock($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fill_stroke {
    my $self = shift;
    eval {
	PDF_fill_stroke($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fill_textblock {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fill_textblock($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fit_graphics {
    my $self = shift;
    eval {
	PDF_fit_graphics($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fit_image {
    my $self = shift;
    eval {
	PDF_fit_image($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fit_pdi_page {
    my $self = shift;
    eval {
	PDF_fit_pdi_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub fit_table {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fit_table($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fit_textflow {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_fit_textflow($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub fit_textline {
    my $self = shift;
    eval {
	PDF_fit_textline($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub get_apiname {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_apiname($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_buffer {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_buffer($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_errmsg {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_errmsg($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_errnum {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_errnum($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_option {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_option($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_parameter {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_get_parameter(): Deprecated, use PDF_get_option() and PDF_get_string()");
        }
	$ret = PDF_get_parameter($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_pdi_parameter {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_get_pdi_parameter(): Deprecated, use PDF_pcos_get_string()");
        }
	$ret = PDF_get_pdi_parameter($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_pdi_value {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_get_pdi_value(): Deprecated, use PDF_pcos_get_number()");
        }
	$ret = PDF_get_pdi_value($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_string {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_get_string($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub get_value {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_get_value(): Deprecated, use PDF_get_option()");
        }
	$ret = PDF_get_value($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_font {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_font($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_graphics {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_graphics($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_image {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_image($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_matchbox {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_matchbox($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_path {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_path($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_pdi_page {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_pdi_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_pvf {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_pvf($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_table {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_table($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_textflow {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_textflow($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub info_textline {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_info_textline($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub initgraphics {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_initgraphics(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_initgraphics($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub lineto {
    my $self = shift;
    eval {
	PDF_lineto($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub load_3ddata {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_3ddata($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub load_asset {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_asset($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub load_font {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_font($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub load_graphics {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_graphics($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub load_iccprofile {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_iccprofile($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub load_image {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_load_image($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub makespotcolor {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_makespotcolor($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub mc_point {
    my $self = shift;
    eval {
	PDF_mc_point($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub moveto {
    my $self = shift;
    eval {
	PDF_moveto($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub open_pdi {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_open_pdi(): Deprecated, use PDF_open_pdi_document()");
        }
	$ret = PDF_open_pdi($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub open_pdi_document {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_open_pdi_document($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub open_pdi_page {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_open_pdi_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub pcos_get_number {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_pcos_get_number($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub pcos_get_string {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_pcos_get_string($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub pcos_get_stream {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_pcos_get_stream($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub poca_delete {
    my $self = shift;
    eval {
	PDF_poca_delete($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub poca_insert {
    my $self = shift;
    eval {
	PDF_poca_insert($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub poca_new {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_poca_new($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub poca_remove {
    my $self = shift;
    eval {
	PDF_poca_remove($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub process_pdi {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_process_pdi($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub rect {
    my $self = shift;
    eval {
	PDF_rect($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub restore {
    my $self = shift;
    eval {
	PDF_restore($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub resume_page {
    my $self = shift;
    eval {
	PDF_resume_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub rotate {
    my $self = shift;
    eval {
	PDF_rotate($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub save {
    my $self = shift;
    eval {
	PDF_save($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub scale {
    my $self = shift;
    eval {
	PDF_scale($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_graphics_option {
    my $self = shift;
    eval {
	PDF_set_graphics_option($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_gstate {
    my $self = shift;
    eval {
	PDF_set_gstate($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_info {
    my $self = shift;
    eval {
	PDF_set_info($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_layer_dependency {
    my $self = shift;
    eval {
	PDF_set_layer_dependency($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_option {
    my $self = shift;
    eval {
	PDF_set_option($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_parameter {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_set_parameter(): Deprecated, use PDF_set_option(), PDF_set_text_option() and PDF_set_graphics_option()");
        }
	PDF_set_parameter($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_text_option {
    my $self = shift;
    eval {
	PDF_set_text_option($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_text_pos {
    my $self = shift;
    eval {
	PDF_set_text_pos($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub set_value {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_set_value(): Deprecated, use PDF_set_option(), PDF_set_text_option() and PDF_set_graphics_option().");
        }
	PDF_set_value($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setcolor {
    my $self = shift;
    eval {
	PDF_setcolor($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setdash {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setdash(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setdash($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setdashpattern {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setdashpattern(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setdashpattern($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setflat {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setflat(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setflat($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setfont {
    my $self = shift;
    eval {
	PDF_setfont($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setlinecap {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setlinecap(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setlinecap($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setlinejoin {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setlinejoin(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setlinejoin($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setlinewidth {
    my $self = shift;
    eval {
	PDF_setlinewidth($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setmatrix {
    my $self = shift;
    eval {
	PDF_setmatrix($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub setmiterlimit {
    my $self = shift;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_setmiterlimit(): Deprecated, use PDF_set_graphics_option()");
        }
	PDF_setmiterlimit($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub shading {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_shading($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub shading_pattern {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_shading_pattern($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub shfill {
    my $self = shift;
    eval {
	PDF_shfill($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub show {
    my $self = shift;
    eval {
	PDF_show($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub show_boxed {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_show_boxed(): Deprecated, use PDF_fit_textline() or PDF_fit_textflow()");
        }
	$ret = PDF_show_boxed($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub show_xy {
    my $self = shift;
    eval {
	PDF_show_xy($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub skew {
    my $self = shift;
    eval {
	PDF_skew($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub stringwidth {
    my $self = shift;
    my $ret;
    eval {
	$ret = PDF_stringwidth($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub stroke {
    my $self = shift;
    eval {
	PDF_stroke($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub suspend_page {
    my $self = shift;
    eval {
	PDF_suspend_page($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub translate {
    my $self = shift;
    eval {
	PDF_translate($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
}

sub utf16_to_utf8 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf16_to_utf8(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf16_to_utf8($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub utf8_to_utf16 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf8_to_utf16(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf8_to_utf16($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub utf32_to_utf8 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf32_to_utf8(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf32_to_utf8($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub utf8_to_utf32 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf8_to_utf32(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf8_to_utf32($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub utf16_to_utf32 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf16_to_utf32(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf16_to_utf32($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}

sub utf32_to_utf16 {
    my $self = shift;
    my $ret;
    eval {
        if (warnings::enabled("deprecated")) {
            warnings::warn("PDF_utf32_to_utf16(): Deprecated, use PDF_convert_to_unicode()");
        }
	$ret = PDF_utf32_to_utf16($self->{pdf}, @_);
    };
    if ($@) {
	croak($@);
    }
    return($ret);
}
