# frozen_string_literal: true

# Blacklight controller that handles searches and document requests
class CatalogController < ApplicationController

  include Blacklight::Catalog
  include BlacklightRangeLimit::ControllerOverride

  include BlacklightRangeLimit::ControllerOverride

  # include BlacklightMaps::Controller


  configure_blacklight do |config|
    
    config.bootstrap_version = 5

    #Add advanced search fields
    config.advanced_search.enabled = true

    # Field that contains geospatial information
    config.view.maps.geojson_field = 'coordinate_location'
  
    ## Default parameters to send to solr for all search-like requests. See also SearchBuilder#processed_parameters
    config.default_solr_params = {
      :rows => 10,
      :fl => '*,score',
      :defType => 'edismax',
      :wt => 'json',
      :qt => 'conflicts'  # Make sure this points to the correct Solr core
    }

    # Maximum number of results to show per page
    config.max_per_page = 20
    # Options for the user for number of results to show per page
    config.per_page = [10, 20, 30, 40]
    

    # solr field configuration for search results/index views
    config.index.title_field = 'label'
    config.index.display_type_field = 'display_type'
    config.index.thumbnail_field = 'image'
    config.index.thumbnail_size = '50x50' # Set the size you want here

    # Solr field configuration for document/show views
    config.show.title_field = 'label'
    config.show.display_type_field = 'display_type'
    config.show.thumbnail_field = 'image'
    config.show.thumbnail_size = '50x50'

    # Solr fields to be displayed in the index (search results) view

    config.add_index_field 'date', label: 'Date', helper_method: :show_date
    config.add_index_field 'summary', label: 'Summary', helper_method: :summarize_summary
    config.add_index_field 'participants', label: 'Participants'
    config.add_index_field 'participants_count', label: 'Participants Count'
    config.add_index_field 'country', label: 'Country'
    config.add_index_field 'instance_of', label: 'Instance Of'
    config.add_index_field 'location', label: 'Location'
    config.add_index_field 'part_of', label: 'Part Of', helper_method: :link_to_part_of
    config.add_index_field 'coordinate_location', label: 'Coordinate Location', helper_method: :link_to_coordinate_location

    # Solr fields to be displayed in the show (single result) view
    config.add_show_field 'date', label: 'Date', helper_method: :show_date
    config.add_show_field 'article', label: 'Wikipedia Article', helper_method: :link_to_article
    config.add_show_field 'event', label: 'Wikidata Event', helper_method: :link_to_event
    config.add_show_field 'summary', label: 'Summary'
    config.add_show_field 'participants', label: 'Participants'
    config.add_show_field 'participants_count', label: 'Participants Count'
    config.add_show_field 'country', label: 'Country'
    config.add_show_field 'instance_of', label: 'Instance Of'
    config.add_show_field 'location', label: 'Location'
    config.add_show_field 'part_of', label: 'Part Of', helper_method: :link_to_part_of
    config.add_show_field 'coordinate_location', label: 'Coordinate Location', helper_method: :link_to_coordinate_location
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
    #config.add_show_field 'start_time', label: 'Start Time'
    config.add_show_field 'official_name', label: 'Official Name'
    config.add_show_field 'said_to_be_the_same_as', label: 'Said To Be The Same As'
    config.add_show_field 'significant_event', label: 'Significant Event'
    config.add_show_field 'followed_by', label: 'Followed By'
    config.add_show_field 'duration', label: 'Duration'
    config.add_show_field 'depicted_by', label: 'Depicted By'
    config.add_show_field 'has_cause', label: 'Has Cause'
    config.add_show_field 'conflict', label: 'Conflict'
    config.add_show_field 'target', label: 'Target'
    #config.add_show_field 'end_time', label: 'End Time'

    # Search fields
    config.add_search_field 'all_fields' do |field|
      field.label = 'All Fields'
      field.solr_parameters = {
        qf: 'label^100 participants^80 part_of^80 country^50 location^50  summary^20',
      }
    end

    config.add_search_field('label') do |field|
      field.label = 'Label'
      field.solr_parameters = {
        qf: 'label',
      }
    end

    config.add_search_field('part_of') do |field|
      field.label = 'Part Of'
      field.solr_parameters = {
        qf: 'part_of',
      }
    end

    config.add_search_field('summary') do |field|
      field.label = 'Summary'
      field.solr_parameters = {
        qf: 'summary',
      }
    end

    # Facet fields
    #For this to work, we will probably need to add a year field to the data, type int, in Solr
    #config.add_facet_field 'date', label: 'Date Year', **default_range_config

    config.add_facet_field :date, label: 'Date',
    query: {
      last_50_years: { label: 'Last 50 Years', fq: 'date:[NOW-50YEAR/DAY TO NOW/DAY]' },
      last_100_years: { label: 'Last 100 Years', fq: 'date:[NOW-100YEAR/DAY TO NOW/DAY]' },
      last_500_years: { label: 'Last 500 Years', fq: 'date:[NOW-500YEAR/DAY TO NOW/DAY]' },
      last_1000_years: { label: 'Last 1000 Years', fq: 'date:[NOW-1000YEAR/DAY TO NOW/DAY]' }
    }, collapse: false
    config.add_facet_field 'label', index_range: 'A'..'Z', limit: 5, collapse: false
    config.add_facet_field 'country', label: 'Country', index_range: 'A'..'Z', limit: 5, collapse: false
    
    config.add_facet_fields_to_solr_request!
  end
end