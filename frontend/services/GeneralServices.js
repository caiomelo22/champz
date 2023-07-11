export default class Service {
  get_image_path(path) {
    return `${process.env.VUE_APP_MEDIA_URL}${path}`
  }
}