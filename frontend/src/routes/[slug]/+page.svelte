<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module, portal, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Tags from '$lib/tags.svelte';
	import Toggle from '$lib/toggle.svelte';

	import Title from './_title.svelte';
	import Description from './_description.svelte';
	import Edit_Tags from './_tags.svelte';
	import Edit_Content from './_content.svelte';
	import Edit_Date from './_date.svelte';
	import Edit_Status from './_status.svelte';
	import Manage_Photo from './_photo.svelte';
	import Manage_Video from './_video.svelte';

	import Share from './_share.svelte';
	import Rating from './__add_rating__.svelte';

	import Comment from './comment.svelte';
	import Highlight from './highlight.svelte';
	import Author from './author.svelte';

	export let data;
	let { post } = data;
	let content = '';
	let tags = [];
	let comments = [];
	let ratings = [];
	let photo_count = 1;
	let video_count = 0;

	$: if ($portal) {
		if ($portal.for == 'post') {
			post = $portal.data;
		} else if ($portal.for == 'comment') {
			comments = $portal.data;
		} else if ($portal.for == 'rating') {
			ratings = $portal.data;
		}

		$portal = {};
	}

	$: {
		content = post.content;
		photo_count = 1;
		let exist = content.search(/{#photo}/) >= 0;
		while (exist) {
			let i = `![${post.title}](${post.photos[photo_count]})`;
			console.log(i);
			content = content.replace(/{#photo}/, i);
			exist = content.search(/{#photo}/) >= 0;
			photo_count = photo_count + 1;
		}

		video_count = 0;
		exist = content.search(/{#video}/) >= 0;
		while (exist) {
			let i = `<iframe
					width="100%"
					height="500px"
					frameborder="0"
					src="https://www.youtube.com/embed/${post.videos[video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, i);
			exist = content.search(/{#video}/) >= 0;
			video_count = video_count + 1;
		}
	}

	// let ratings_value = 0;
	// $: {
	// 	ratings_value = 0;
	// 	for (const i in ratings) {
	// 		ratings_value += ratings[i].rating;
	// 	}
	// }

	let edit_mode = false;
	edit_mode = true;

	let is_admin = $user.permissions.some((x) =>
		[
			'post:edit_status',
			'post:edit_name',
			'post:edit_tag',
			'post:edit_price',
			'post:edit_info',
			'post:edit_variation'
		].includes(x)
	);

	onMount(() => {
		if ($page.url.searchParams.has('edit') && is_admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
	});
</script>

<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	{#if is_admin}
		<Toggle
			state_1="off"
			state_2="edit"
			active={edit_mode}
			on:click={() => {
				edit_mode = !edit_mode;
			}}
		/>
	{/if}
	<img src={post.photos[0] || ''} alt={post.title} onerror="this.src='/site/no_photo.png'" />

	{#if $user.permissions.includes('post:edit_photos') && edit_mode}
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Manage_Photo,
						post,
						photo_count
					};
				}}>Manage Photo</Button
			>

			{#if video_count > 0}
				<Button
					class="tiny"
					on:click={() => {
						$module = {
							module: Manage_Video,
							post,
							video_count
						};
					}}>Manage Video</Button
				>
			{/if}
		</div>
	{/if}

	<br />
	<strong class="big">{post.title}</strong>
	{#if $user.permissions.includes('post:edit_title') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Title,
					post
				};
			}}
		>
			title
		</Button>
	{/if}

	<br />
	<span class="date">{post.date.split('T')[0]}</span>
	{#if $user.permissions.includes('post:edit_date') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Date,
					post
				};
			}}
		>
			date
		</Button>
	{/if}

	{#if $user.permissions.includes('post:edit_description') && edit_mode}
		<br /><br />
		{post.description}

		<Button
			icon="edit"
			class="tiny"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Description,
					post
				};
			}}
		>
			description
		</Button>
	{/if}

	<br /><br />
	{#if $user.permissions.includes('post:edit_content') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Content,
					post
				};
			}}
		>
			content
		</Button>
	{/if}
	<Marked md={content} />
	<br />
	<div class="hr" />

	{#if $user.permissions.includes('post:edit_tags') && edit_mode}
		<br />
		<Button
			icon="edit"
			class="tiny"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Tags,
					post,
					tags_in: tags
				};
			}}
		>
			tags
		</Button>
	{/if}
	{#if post.tags.length > 0}
		<br />
		<Tags tags={post.tags} />
		<br />
		<div class="hr" />
	{/if}
	<br />
	<Author />

	{#if $user.permissions.includes('post:edit_status') && edit_mode}
		<br /> <br />
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Edit_Status,
						post
					};
				}}
			>
				<span>
					Status: <strong>{post.status}</strong>
				</span>
				| Edit
			</Button>
			{#if post.status == 'publish'}
				<Highlight {post} />
			{/if}
		</div>
	{/if}

	<br /><br />

	<!-- {#if $user.login}
		<Button
			class="tiny"
			name="Overall Rating: {ratings_value}"
			icon="heart"
			on:click={() => {
				$module = {
					module: Rating,
					post_key: post.key,
					ratings
				};
			}}
		/>
	{/if} -->

	<Button
		class="tiny"
		name="share"
		icon="share"
		on:click={() => {
			$module = {
				module: Share,
				post
			};
		}}
	/>
	<br /><br /><br />
</Content>

<Comment {comments} post_key={post.key} />
<br /><br />

<style>
	.big {
		font-size: x-large;
		color: var(--ac1);
	}
	img {
		background-color: var(--ac4);
	}
</style>
