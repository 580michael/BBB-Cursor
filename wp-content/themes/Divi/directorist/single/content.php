<?php
/**
 * @package Directorist
 * @since 7.0.5.3
 * Template overridden by BBB
 */

if (!defined('ABSPATH')) {
    exit;
}

$listing = get_post();
$listing_type = get_post_meta($listing->ID, '_directory_type', true);

// Get Divi Builder content if it exists
$divi_content = get_post_meta($listing->ID, '_et_pb_use_builder', true);
$is_divi_layout = !empty($divi_content) && 'on' === $divi_content;

if ($is_divi_layout) {
    // Use Divi Builder content
    echo do_shortcode('[et_pb_section global_module="' . esc_attr(get_post_meta($listing->ID, '_et_pb_layout_id', true)) . '"]');
} else {
    // Fallback to default template
    ?>
    <div class="directorist-single-wrapper">
        <div class="directorist-single-listing">
            <div class="directorist-card directorist-single-listing-header">
                <div class="directorist-card__header">
                    <h2><?php echo esc_html($listing->post_title); ?></h2>
                </div>
                <div class="directorist-card__body">
                    <div class="directorist-listing-details">
                        <?php if ('state' === $listing_type): ?>
                            <!-- State Template -->
                            <div class="state-info">
                                <h3>State Information</h3>
                                <p>Population: <?php echo esc_html(get_post_meta($listing->ID, 'population', true)); ?></p>
                                <div class="emergency-contacts">
                                    <h4>Emergency Contact</h4>
                                    <p><?php echo esc_html(get_post_meta($listing->ID, 'emergency_contact', true)); ?></p>
                                </div>
                            </div>
                        <?php elseif ('county' === $listing_type): ?>
                            <!-- County Template -->
                            <div class="county-info">
                                <h3>County Information</h3>
                                <div class="courthouse-info">
                                    <h4>Courthouse Information</h4>
                                    <p>Address: <?php echo esc_html(get_post_meta($listing->ID, 'courthouse_address', true)); ?></p>
                                    <p>Hours: <?php echo esc_html(get_post_meta($listing->ID, 'courthouse_hours', true)); ?></p>
                                </div>
                            </div>
                        <?php endif; ?>
                        
                        <div class="listing-description">
                            <?php echo wp_kses_post($listing->post_content); ?>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php
}
?> 