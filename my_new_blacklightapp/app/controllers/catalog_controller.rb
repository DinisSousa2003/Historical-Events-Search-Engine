# frozen_string_literal: true

# Blacklight controller that handles searches and document requests
class CatalogController < ApplicationController

  include Blacklight::Catalog
  include BlacklightMaps::Controller


  configure_blacklight do |config|
    
    config.bootstrap_version = 5

    # Field that contains geospatial information
    config.view.maps.geojson_field = 'coordinate_location'
  
    ## Default parameters to send to solr for all search-like requests. See also SearchBuilder#processed_parameters
    config.default_solr_params = {
      :qt => 'search',
      :rows => 10 
    }

    private

    # solr field configuration for search results/index views
    config.index.title_field = 'label'
    config.index.display_type_field = 'format'
    config.index.thumbnail_field = 'image'
    config.index.thumbnail_size = '50x50' # Set the size you want here
    #config.index.thumbnail_method = :render_thumbnail

    # Solr field configuration for document/show views
    config.show.title_field = 'label'
    config.show.display_type_field = 'format'
    config.show.thumbnail_field = 'image'
    config.show.thumbnail_size = '50x50'

    # Solr fields to be displayed in the show (single result) view
    config.add_show_field 'event', label: 'Event'
    config.add_show_field 'date', label: 'Date', date: true
    config.add_show_field 'label', label: 'Label'
    config.add_show_field 'article', label: 'Article'
    config.add_show_field 'summary', label: 'Summary'
    config.add_show_field 'participants', label: 'Participants'
    config.add_show_field 'participants_count', label: 'Participants Count'
    config.add_show_field 'country', label: 'Country'
    config.add_show_field 'instance_of', label: 'Instance Of'
    config.add_show_field 'location', label: 'Location'
    config.add_show_field 'part_of', label: 'Part Of'
    config.add_show_field 'point_in_time', label: 'Point In Time', date: true
    config.add_show_field 'coordinate_location', label: 'Coordinate Location'
    config.add_show_field 'day_in_year_for_periodic_occurrence', label: 'Day In Year for Periodic Occurrence'
    config.add_show_field 'time_period', label: 'Time Period'
    config.add_show_field 'located_in_on_physical_feature', label: 'Located In on Physical Feature'
    config.add_show_field 'topics_main_category', label: 'Topics Main Category'
    config.add_show_field 'main_subject', label: 'Main Subject'
    config.add_show_field 'facet_of', label: 'Facet Of'
    config.add_show_field 'named_after', label: 'Named After'
    config.add_show_field 'significant_person', label: 'Significant Person'
    config.add_show_field 'commanded_by', label: 'Commanded By'
    config.add_show_field 'organizer', label: 'Organizer'
    config.add_show_field 'has_effect', label: 'Has Effect'
    config.add_show_field 'follows', label: 'Follows'
    config.add_show_field 'present_in_work', label: 'Present In Work'
    config.add_show_field 'destroyed', label: 'Destroyed'
    config.add_show_field 'perpetrator', label: 'Perpetrator'
    config.add_show_field 'in_opposition_to', label: 'In Opposition To'
    config.add_show_field 'signatory', label: 'Signatory'
    config.add_show_field 'inception', label: 'Inception'
    config.add_show_field 'short_name', label: 'Short Name'
    config.add_show_field 'start_time', label: 'Start Time'
    config.add_show_field 'official_name', label: 'Official Name'
    config.add_show_field 'said_to_be_the_same_as', label: 'Said To Be The Same As'
    config.add_show_field 'significant_event', label: 'Significant Event'
    config.add_show_field 'followed_by', label: 'Followed By'
    config.add_show_field 'duration', label: 'Duration'
    config.add_show_field 'depicted_by', label: 'Depicted By'
    config.add_show_field 'has_cause', label: 'Has Cause'
    config.add_show_field 'conflict', label: 'Conflict'
    config.add_show_field 'target', label: 'Target'
    config.add_show_field 'end_time', label: 'End Time'

    # Search fields
    config.add_search_field 'all_fields', label: 'All Fields'

    config.add_search_field('label') do |field|
      field.label = 'Label'
      field.solr_parameters = {
        'spellcheck.dictionary': 'label',
        qf: '${label_qf}',
        pf: '${label_pf}'
      }
      field.clause_params = {
        edismax: field.solr_parameters.dup # use the same title fields for advanced title search as for regular title search
      }
    end

    config.add_search_field('summary') do |field|
      field.label = 'Summary'
      field.solr_parameters = {
        'spellcheck.dictionary': 'summary',
        qf: '${summary_qf}',
        pf: '${summary_pf}'
      }
    end

    # Facet fields
    configure_blacklight do |config|
      config.add_facet_field 'part_of', label: 'Part Of', show:true, collapsing: true
    end

    # Sort fields
    configure_blacklight do |config|
      config.add_sort_field 'relevance', sort: 'score desc, date desc, label asc', label: 'Relevance'
      config.add_sort_field 'date-desc', sort: 'date desc, label asc', label: 'Date'
      config.add_sort_field 'date-asc', sort: 'date asc, label asc', label: 'Date'
    end

    # Solr fields to be displayed in the index (search results) view

    config.add_index_field 'date', label: 'Date', date: {format: :short}
    config.add_index_field 'article', label: 'Article'
    config.add_index_field 'summary', label: 'Summary'
    config.add_index_field 'participants', label: 'Participants'
    config.add_index_field 'participants_count', label: 'Participants Count'
    config.add_index_field 'country', label: 'Country'
    config.add_index_field 'instance_of', label: 'Instance Of'
    config.add_index_field 'location', label: 'Location'
    config.add_index_field 'part_of', label: 'Part Of'
  end
end