module ApplicationHelper
    # app/helpers/application_helper.rb
    def render_thumbnail(document, options)
        return unless document[:file_id].present?
        image_tag(
        "#{image_server}/#{document.id}/#{document.first(:file_id)}.png",
        options.merge(alt: presenter(document).document_heading)
        )
    end
end
