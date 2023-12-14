# frozen_string_literal: true

# Blacklight controller that handles searches and document requests
class CatalogController < ApplicationController

  include Blacklight::Catalog
  include Blacklight::Marc::Catalog


  # If you'd like to handle errors returned by Solr in a certain way,
  # you can use Rails rescue_from with a method you define in this controller,
  # uncomment:
  #
  # rescue_from Blacklight::Exceptions::InvalidRequest, with: :my_handling_method

  configure_blacklight do |config|
    ## Specify the style of markup to be generated (may be 4 or 5)
    config.bootstrap_version = 5
    #
    ## Class for sending and receiving requests from a search index
    config.repository_class = Blacklight::Solr::Repository
    #
    ## Class for converting Blacklight's url parameters to into request parameters for the search index
    config.search_builder_class = ::SearchBuilder
    #
    ## Model that maps search index responses to the blacklight response model
    config.response_model = Blacklight::Solr::Response
    #
    ## The destination for the link around the logo in the header
    # config.logo_link = root_path
    #
    ## Should the raw solr document endpoint (e.g. /catalog/:id/raw) be enabled
    config.raw_endpoint.enabled = false

    ## Default parameters to send to solr for all search-like requests. See also SearchBuilder#processed_parameters
    config.default_solr_params = {
      rows: 10,
      :fl => '*,score',
      :defType => 'edismax',
      :wt => 'json',
      :qt => 'conflicts'
    }

    # solr path which will be added to solr base url before the other solr params.
    #config.solr_path = 'select'
    #config.document_solr_path = 'get'
    #config.json_solr_path = 'advanced'

    # Maximum number of results to show per page
    config.max_per_page = 20
    # items to show per page, each number in the array represent another option to choose from.
    config.per_page = [10,20,50,100]

    # solr field configuration for search results/index views
    config.index.title_field = 'label'
    config.index.display_type_field = 'display_type'
    config.index.thumbnail_field = 'image'
    config.index.thumbnail_size = '50x50' # Set the size you want here

    # The presenter is the view-model class for the page
    # config.index.document_presenter_class = MyApp::IndexPresenter

    # Some components can be configured
    # config.index.document_component = MyApp::SearchResultComponent
    # config.index.constraints_component = MyApp::ConstraintsComponent
    # config.index.search_bar_component = MyApp::SearchBarComponent
    # config.index.search_header_component = MyApp::SearchHeaderComponent
    config.index.document_actions.delete(:bookmark)

    config.add_results_document_tool(:bookmark, component: Blacklight::Document::BookmarkComponent, if: :render_bookmarks_control?)

    config.add_results_collection_tool(:sort_widget)
    config.add_results_collection_tool(:per_page_widget)
    config.add_results_collection_tool(:view_type_group)

    config.add_show_tools_partial(:bookmark, component: Blacklight::Document::BookmarkComponent, if: :render_bookmarks_control?)
    # config.add_show_tools_partial(:email, callback: :email_action, validator: :validate_email_params)
    # config.add_show_tools_partial(:sms, if: :render_sms_action?, callback: :sms_action, validator: :validate_sms_params)
    # config.add_show_tools_partial(:citation)

    config.add_nav_action(:bookmark, partial: 'blacklight/nav/bookmark', if: :render_bookmarks_control?)
    config.add_nav_action(:search_history, partial: 'blacklight/nav/search_history')

    # solr field configuration for document/show views
    config.show.title_field = 'label'
    config.show.display_type_field = 'display_type'
    config.show.thumbnail_field = 'image'
    config.show.thumbnail_size = '50x50'

    #Add advanced search fields
    config.advanced_search.enabled = true

    #
    # The presenter is a view-model class for the page
    # config.show.document_presenter_class = MyApp::ShowPresenter
    #
    # These components can be configured
    # config.show.document_component = MyApp::DocumentComponent
    # config.show.sidebar_component = MyApp::SidebarComponent
    # config.show.embed_component = MyApp::EmbedComponent

    # solr fields that will be treated as facets by the blacklight application
    #   The ordering of the field names is the order of the display
    #
    # Setting a limit will trigger Blacklight's 'more' facet values link.
    # * If left unset, then all facet values returned by solr will be displayed.
    # * If set to an integer, then "f.somefield.facet.limit" will be added to
    # solr request, with actual solr request being +1 your configured limit --
    # you configure the number of items you actually want _displayed_ in a page.
    # * If set to 'true', then no additional parameters will be sent to solr,
    # but any 'sniffed' request limit parameters will be used for paging, with
    # paging at requested limit -1. Can sniff from facet.limit or
    # f.specific_field.facet.limit solr request params. This 'true' config
    # can be used if you set limits in :default_solr_params, or as defaults
    # on the solr side in the request handler itself. Request handler defaults
    # sniffing requires solr requests to be made with "echoParams=all", for
    # app code to actually have it echo'd back to see it.
    #
    # :show may be set to false if you don't want the facet to be drawn in the
    # facet bar
    #
    # set :index_range to true if you want the facet pagination view to have facet prefix-based navigation
    #  (useful when user clicks "more" on a large facet and wants to navigate alphabetically across a large set of results)
    # :index_range can be an array or range of prefixes that will be used to create the navigation (note: It is case sensitive when searching values)

    # config.add_facet_field 'format', label: 'Format'
    # config.add_facet_field 'pub_date_ssim', label: 'Publication Year', single: true
    # config.add_facet_field 'subject_ssim', label: 'Topic', limit: 20, index_range: 'A'..'Z'
    # config.add_facet_field 'language_ssim', label: 'Language', limit: true
    # config.add_facet_field 'lc_1letter_ssim', label: 'Call Number'
    # config.add_facet_field 'subject_geo_ssim', label: 'Region'
    # config.add_facet_field 'subject_era_ssim', label: 'Era'

    # config.add_facet_field 'example_pivot_field', label: 'Pivot Field', pivot: ['format', 'language_ssim'], collapsing: true

    # config.add_facet_field 'example_query_facet_field', label: 'Publish Date', :query => {
    #    :years_5 => { label: 'within 5 Years', fq: "pub_date_ssim:[#{Time.zone.now.year - 5 } TO *]" },
    #    :years_10 => { label: 'within 10 Years', fq: "pub_date_ssim:[#{Time.zone.now.year - 10 } TO *]" },
    #    :years_25 => { label: 'within 25 Years', fq: "pub_date_ssim:[#{Time.zone.now.year - 25 } TO *]" }
    # }

    config.add_facet_field :date, label: 'Date',
    query: {
      :last_50_years => { label: 'Last 50 Years', fq: 'date:[NOW-50YEAR/DAY TO NOW/DAY]' },
      :last_100_years => { label: 'Last 100 Years', fq: 'date:[NOW-100YEAR/DAY TO NOW/DAY]' },
      :last_500_years => { label: 'Last 500 Years', fq: 'date:[NOW-500YEAR/DAY TO NOW/DAY]' },
      :last_1000_years => { label: 'Last 1000 Years', fq: 'date:[NOW-1000YEAR/DAY TO NOW/DAY]' }
    }
    config.add_facet_field 'label', index_range: 'A'..'Z', limit: 5
    config.add_facet_field 'country', label: 'Country', index_range: 'A'..'Z', limit: 5


    # Have BL send all facet field names to Solr, which has been the default
    # previously. Simply remove these lines if you'd rather use Solr request
    # handler defaults, or have no facets.
    config.add_facet_fields_to_solr_request!

    # solr fields to be displayed in the index (search results) view
    #   The ordering of the field names is the order of the display
    # config.add_index_field 'title_tsim', label: 'Title'
    # config.add_index_field 'title_vern_ssim', label: 'Title'
    # config.add_index_field 'author_tsim', label: 'Author'
    # config.add_index_field 'author_vern_ssim', label: 'Author'
    # config.add_index_field 'format', label: 'Format'
    # config.add_index_field 'language_ssim', label: 'Language'
    # config.add_index_field 'published_ssim', label: 'Published'
    # config.add_index_field 'published_vern_ssim', label: 'Published'
    # config.add_index_field 'lc_callnum_ssim', label: 'Call number'

    config.add_index_field 'date', label: 'Date', helper_method: :show_date
    config.add_index_field 'summary', label: 'Summary', helper_method: :summarize_summary
    config.add_index_field 'participants', label: 'Participants'
    config.add_index_field 'participants_count', label: 'Participants Count'
    config.add_index_field 'country', label: 'Country'
    config.add_index_field 'instance_of', label: 'Instance Of'
    config.add_index_field 'location', label: 'Location'
    config.add_index_field 'part_of', label: 'Part Of', helper_method: :link_to_part_of
    config.add_index_field 'coordinate_location', label: 'Coordinate Location', helper_method: :link_to_coordinate_location


    # solr fields to be displayed in the show (single result) view
    #   The ordering of the field names is the order of the display
    # config.add_show_field 'title_tsim', label: 'Title'
    # config.add_show_field 'title_vern_ssim', label: 'Title'
    # config.add_show_field 'subtitle_tsim', label: 'Subtitle'
    # config.add_show_field 'subtitle_vern_ssim', label: 'Subtitle'
    # config.add_show_field 'author_tsim', label: 'Author'
    # config.add_show_field 'author_vern_ssim', label: 'Author'
    # config.add_show_field 'format', label: 'Format'
    # config.add_show_field 'url_fulltext_ssim', label: 'URL'
    # config.add_show_field 'url_suppl_ssim', label: 'More Information'
    # config.add_show_field 'language_ssim', label: 'Language'
    # config.add_show_field 'published_ssim', label: 'Published'
    # config.add_show_field 'published_vern_ssim', label: 'Published'
    # config.add_show_field 'lc_callnum_ssim', label: 'Call number'
    # config.add_show_field 'isbn_ssim', label: 'ISBN'

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

    # "fielded" search configuration. Used by pulldown among other places.
    # For supported keys in hash, see rdoc for Blacklight::SearchFields
    #
    # Search fields will inherit the :qt solr request handler from
    # config[:default_solr_parameters], OR can specify a different one
    # with a :qt key/value. Below examples inherit, except for subject
    # that specifies the same :qt as default for our own internal
    # testing purposes.
    #
    # The :key is what will be used to identify this BL search field internally,
    # as well as in URLs -- so changing it after deployment may break bookmarked
    # urls.  A display label will be automatically calculated from the :key,
    # or can be specified manually to be different.

    # This one uses all the defaults set by the solr request handler. Which
    # solr request handler? The one set in config[:default_solr_parameters][:qt],
    # since we aren't specifying it otherwise.

    # config.add_search_field 'all_fields', label: 'All Fields'

    


    # Now we see how to over-ride Solr request handler defaults, in this
    # case for a BL "search field", which is really a dismax aggregate
    # of Solr search fields.

    # config.add_search_field('title') do |field|
    #   # solr_parameters hash are sent to Solr as ordinary url query params.
    #   field.solr_parameters = {
    #     'spellcheck.dictionary': 'title',
    #     qf: '${title_qf}',
    #     pf: '${title_pf}'
    #   }
    # end

    # config.add_search_field('author') do |field|
    #   field.solr_parameters = {
    #     'spellcheck.dictionary': 'author',
    #     qf: '${author_qf}',
    #     pf: '${author_pf}'
    #   }
    # end

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

    # Specifying a :qt only to show it's possible, and so our internal automated
    # tests can test it. In this case it's the same as
    # config[:default_solr_parameters][:qt], so isn't actually neccesary.
    # config.add_search_field('subject') do |field|
    #   field.qt = 'search'
    #   field.solr_parameters = {
    #     'spellcheck.dictionary': 'subject',
    #     qf: '${subject_qf}',
    #     pf: '${subject_pf}'
    #   }
    # end

    # "sort results by" select (pulldown)
    # label in pulldown is followed by the name of the Solr field to sort by and
    # whether the sort is ascending or descending (it must be asc or desc
    # except in the relevancy case). Add the sort: option to configure a
    # custom Blacklight url parameter value separate from the Solr sort fields.
    config.add_sort_field '', sort: '', label: 'none'
    config.add_sort_field 'date', sort: 'date desc', label: 'date'
    config.add_sort_field 'label', sort: 'label asc', label: 'name'
    # config.add_sort_field 'year-desc', sort: 'pub_date_si desc, title_si asc', label: 'year'
    # config.add_sort_field 'author', sort: 'author_si asc, title_si asc', label: 'author'
    # config.add_sort_field 'title_si asc, pub_date_si desc', label: 'title'

    # If there are more than this many search results, no spelling ("did you
    # mean") suggestion is offered.
    config.spell_max = 5

    # Configuration for autocomplete suggester
    config.autocomplete_enabled = true
    config.autocomplete_path = 'suggest'
    # if the name of the solr.SuggestComponent provided in your solrconfig.xml is not the
    # default 'mySuggester', uncomment and provide it below
    # config.autocomplete_suggester = 'mySuggester'
  end
end
