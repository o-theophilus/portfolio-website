<script>
	import { api_url, module, _portal, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Tags from '$lib/tags.svelte';

	import Delete from './__delete__.svelte';
	import Title from './__edit_title__.svelte';
	import Description from './__edit_description__.svelte';
	import Edit_Tags from './__edit_tags__.svelte';
	import Edit_Content from './__edit_content__.svelte';
	import Edit_Date from './__edit_date__.svelte';
	import Edit_Status from './__edit_status__.svelte';
	import Manage_Photo from './__manage_photo__.svelte';
	import Manage_Video from './__manage_video__.svelte';
	import Share from './__share__.svelte';
	import Rating from './__add_rating__.svelte';
	import Comment from './comment.svelte';
	import Author from './author.svelte';

	export let data;
	let { post } = data;
	let { tags } = data;
	let { comments } = data;
	let { ratings } = data;

	$: if ($_portal) {
		if ($_portal.for == 'post') {
			post = $_portal.data;
		} else if ($_portal.for == 'comment') {
			comments = $_portal.data;
		} else if ($_portal.for == 'rating') {
			ratings = $_portal.data;
		}

		$_portal = {};
	}

	let content = post.content;
	$: {
		content = post.content;
		post.photo_count = 1;
		let is_available = content.search(/{#photo}/) >= 0;
		while (is_available) {
			let photo = `![${post.title}](${api_url}/${post.photos[post.photo_count]})`;
			content = content.replace(/{#photo}/, photo);
			is_available = content.search(/{#photo}/) >= 0;
			post.photo_count = post.photo_count + 1;
		}
	}

	$: {
		post.video_count = 0;
		let is_available = content.search(/{#video}/) >= 0;
		while (is_available) {
			let v = `<iframe 
					width="100%" 
					height="500px"
					frameborder="0" 
					src="https://www.youtube.com/embed/${post.videos[post.video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, v);
			is_available = content.search(/{#video}/) >= 0;
			post.video_count = post.video_count + 1;
		}
	}

	let ratings_value = 0;
	$: {
		ratings_value = 0;
		for (const i in ratings) {
			ratings_value += ratings[i].rating;
		}
	}

	let edit_mode = false;
</script>

<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	{#if $_user.roles.includes('admin')}
		<Button
			class="tiny"
			on:click={() => {
				edit_mode = !edit_mode;
			}}>Edit Mode: {edit_mode}</Button
		>
		<br />
		<br />
	{/if}
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>

	{#if $_user.roles.includes('admin') && edit_mode}
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Manage_Photo,
						post
					};
				}}>Manage Photo</Button
			>
			{#if post.video_count > 0}
				<Button
					class="tiny"
					on:click={() => {
						$module = {
							module: Manage_Video,
							post
						};
					}}>Manage Video</Button
				>
			{/if}
		</div>
	{/if}

	<br />
	<strong class="big">{post.title}</strong>
	{#if $_user.roles.includes('admin') && edit_mode}
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
	<span class="date">{post.created_at.split('T')[0]}</span>
	{#if $_user.roles.includes('admin') && edit_mode}
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

	{#if $_user.roles.includes('admin') && edit_mode}
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
	{#if $_user.roles.includes('admin') && edit_mode}
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

	{#if $_user.roles.includes('admin') && edit_mode}
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
	{/if}
	<Tags tags={post.tags} />
	<br /><br />
	<Author />

	{#if $_user.roles.includes('admin') && edit_mode}
		<br /> <br />
		Status: <strong> {post.status}</strong>
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Edit_Status,
						post
					};
				}}>Edit Status</Button
			>
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Delete,
						post
					};
				}}>Delete</Button
			>
		</div>
	{/if}

	<br /><br />

	{#if $_user.login}
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
	{/if}

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
		color: var(--accent1);
	}
	img {
		background-color: var(--accent4);
	}
</style>
