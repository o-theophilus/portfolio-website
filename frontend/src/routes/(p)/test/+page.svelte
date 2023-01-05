<script>
	import Video from '$lib/module/add_photo_many.svelte';
	import Content from '$lib/comp/content.svelte';

	let data = {
		post: {},
		post_type: 'platy'
	};
</script>

<Content>
	<Video {data} />
</Content>
