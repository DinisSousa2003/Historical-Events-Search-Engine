# app/helpers/custom_layout_helper.rb
module CustomLayoutHelper
    include Blacklight::LayoutHelperBehavior
    
    ##
    # Overriden to include dir
    def html_tag_attributes
        { lang: I18n.locale }
    end
  end