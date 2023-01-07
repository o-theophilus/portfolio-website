<script>
	import Video from '$lib/module/add_photo_many.svelte';
	import Content from '$lib/comp/content.svelte';

	let data = {
		post: {},
		post_type: 'blog'
	};
</script>

<Content>
	<Video {data} />
</Content>
