class StaticPagesController < ApplicationController
  def map_action
    # Get the map from assets map.html and renturn it
    render file: 'public/map.html'
  end
end
