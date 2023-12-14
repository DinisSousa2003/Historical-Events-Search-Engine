# frozen_string_literal: true

# Represents a single document returned from Solr
class SolrDocument
  include Blacklight::Solr::Document
      # The following shows how to setup this blacklight document to display marc documents
  extension_parameters[:marc_source_field] = :marc_ss
  extension_parameters[:marc_format_type] = :marcxml
  use_extension(Blacklight::Marc::DocumentExtension) do |document|
    document.key?(SolrDocument.extension_parameters[:marc_source_field])
  end

  field_semantics.merge!(
                          :event => 'event',
                          :date => 'date',
                          :label => 'label',
                          :image => 'image',
                          :article => 'article',
                          :summary => 'summary',
                          :participants => 'participants',
                          :participants_count => 'participants_count',
                          :country => 'country',
                          :instance_of => 'instance_of',
                          :location => 'location',
                          :part_of => 'part_of',
                          :point_in_time => 'point_in_time',
                          :coordinate_location => 'coordinate_location_m',
                          :day_in_year_for_periodic_occurrence => 'day_in_year_for_periodic_occurrence',
                          :time_period => 'time_period',
                          :located_in_on_physical_feature => 'located_in_on_physical_feature',
                          :topics_main_category => 'topics_main_category',
                          :main_subject => 'main_subject',
                          :facet_of => 'facet_of',
                          :named_after => 'named_after',
                          :significant_person => 'significant_person',
                          :commanded_by => 'commanded_by',
                          :organizer => 'organizer',
                          :has_effect => 'has_effect',
                          :follows => 'follows',
                          :present_in_work => 'present_in_work',
                          :destroyed => 'destroyed',
                          :perpetrator => 'perpetrator',
                          :in_opposition_to => 'in_opposition_to',
                          :signatory => 'signatory',
                          :inception => 'inception_',
                          :short_name => 'short_name',
                          :start_time => 'start_time_',
                          :official_name => 'official_name',
                          :said_to_be_the_same_as => 'said_to_be_the_same_as',
                          :significant_event => 'significant_event',
                          :followed_by => 'followed_by',
                          :duration => 'duration',
                          :depicted_by => 'depicted_by',
                          :has_cause => 'has_cause',
                          :conflict => 'conflict',
                          :target => 'target',
                          :end_time => 'end_time'
                        )



  # self.unique_key = 'event'

  # DublinCore uses the semantic field mappings below to assemble an OAI-compliant Dublin Core document
  # Semantic mappings of solr stored fields. Fields may be multi or
  # single valued. See Blacklight::Document::SemanticFields#field_semantics
  # and Blacklight::Document::SemanticFields#to_semantic_values
  # Recommendation: Use field names from Dublin Core
  use_extension(Blacklight::Document::DublinCore)
end
